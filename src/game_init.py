# -*- coding: utf-8 -*-
"""
Created on Sat May 10 20:33:53 2025

@author: ndagg
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import json

from src.gameObjects.gamemap import BaseMap
from src.gameObjects.player import Player
from src.gameObjects.cos import BlankCO
from src.gameObjects.units import Unit, UNITS, UNIT_NAMES
from src.gameObjects.buildings import (
    Building,
    City,
    Base,
    Airport,
    Port,
    HQ,
    ComTower,
    Lab
)

from src.gameUtils.aw_lists import TERRAIN_TYPES

from src.codeUtils.helpers import loc_2_gloc, match_terrain_name

class GameReader:
    """
    A class for fetching and interpreting game data from amarriner.com
    """
    def __init__(self, driver=None):
        if driver is None:
            self.driver = webdriver.Firefox
        else:
            self.driver = driver

        self.xmax = 0
        self.ymax = 0
    
    def get_html(self, link):
        """
        Retrieve the page source from the link
        """
        self.link = link
        
        # Open the webpage
        driver_instance = self.driver()
        driver_instance.get(link)
        
        # Get the page source (HTML)
        html = driver_instance.page_source
        
        # Always close the driver
        driver_instance.quit()
        
        self.html = BeautifulSoup(html, 'html.parser')
        self.prettied = self.html.prettify()
        
        
    def get_terrain_dict(self):
        """
        Extract the terrain dictionary from the game page HTML
        """
        start = self.prettied.index("terrainInfo")
        terrain_info_text = self.prettied[start+14:].partition(";")[0]
        terrain_dict = json.loads(terrain_info_text)
        self.terrain_dict = terrain_dict
    
    def get_awbw_building_dict(self):
        """
        Extract the building dictionary from the game page HTML
        """
        start = self.prettied.index("buildingsInfo")
        building_info_text = self.prettied[start+16:].partition(";")[0]
        building_dict = json.loads(building_info_text)
        self.awbw_building_dict = building_dict

    def get_unit_dict(self):
        """
        Extract the unit dictionary from the game page HTML
        """
        start = self.prettied.index("unitsInfo")
        units_info_text = self.prettied[start+12:].partition(";")[0]
        unit_dict = json.loads(units_info_text)
        self.unit_dict = unit_dict

    def get_player_dict(self):
        """
        Extract the player info from the game page HTML
        """
        start = self.prettied.index("playersInfo")
        player_info_text = self.prettied[start+14:].partition(";")[0]
        player_dict = json.loads(player_info_text)
        player_dict = {int(k): v for k, v in player_dict.items()}

        self.player_dict = player_dict
    
    def generate_basemap(self) -> BaseMap:
        """
        Generate the BaseMap object for the currently stored game
        """
        self.get_terrain_dict()
        self.get_awbw_building_dict()
        basemap = BaseMap(self.terrain_dict, self.awbw_building_dict)
        self.dims = basemap.dims
        return basemap
    
    def generate_players(self) -> list[Player]:
        """
        Generate the Player and CO objects for the currently stored game
        """
        self.get_player_dict()

        players = []
        self.min_id = min(list(self.player_dict.keys()))
        self.ids = []
        
        for p in self.player_dict.values():
            # TODO - include CO list
            id = int(p["players_id"]) - self.min_id
            self.ids.append(id)
            co = BlankCO(id)
            co.power_meter = p["players_co_power"]
            players.append(Player(id, None, co))
        return players

    def generate_unit_lists(self) -> list[Unit]:
        """
        Generate the Unit lists for the currently stored game
        """
        self.get_unit_dict()
        unit_lists = [[] for i in range(len(self.ids))]

        for k, v in self.unit_dict.items():
            unit = UNIT_NAMES.index(v["units_name"])
            unit = UNITS[unit]()
            unit.fuel = v["units_fuel"]
            unit.hidden = v["units_sub_dive"] != "N"
            if unit.id not in [0, 2]:  # Inf and Recon has infinite ammo
                unit.ammo = v["units_ammo"]
            unit.set_loc((v["units_x"], v["units_y"]), self.dims)
            unit.vhp = v["units_hit_points"]
            if unit.vhp < 10:
                unit.hp = unit.vhp * 10 - 5  # Assumes unit is at mid-point of hp bracket
            unit.active = bool(v["units_moved"])
            owner = int(v["units_players_id"]) - self.min_id
            unit.owner = owner
            # TODO - include transports

            unit_lists[owner].append(unit)
        return unit_lists

    def generate_building_dict(self) -> dict[int: Building]:
        """
        Generate the building dict for the currently stored game
        """
        self.get_awbw_building_dict()
        building_dict = {}
        b_inds = {11: City, 12: Base, 13: Airport, 14: Port, 15: HQ, 16: ComTower, 17: Lab}

        # Get map dimensions
        x_dim = max(
            max(int(i) for i in self.awbw_building_dict.keys()),
            max(int(i) for i in self.terrain_dict.keys())) + 1
        y_dim = max(
            max(int(i) for i in self.awbw_building_dict['0'].keys()),
            max(int(i) for i in self.terrain_dict['0'].keys())) + 1
        
        dims = [x_dim, y_dim]
        
        for x, dict_ in self.awbw_building_dict.items():
            if type(dict_) is list:
                dict_ = {dict_[0]["buildings_y"]: dict_[0]}
            for y, v in dict_.items():
                # Get building type
                building_type = match_terrain_name(v["terrain_name"], TERRAIN_TYPES)
                if building_type not in b_inds.keys():  # Catch things like missile silos
                    continue
                building_type = b_inds[building_type]

                gloc = loc_2_gloc((int(x), int(y)), dims)
                building = building_type(gloc)
                
                # Get attributes
                id = v["buildings_team"]
                if id:
                    building.owner = int(id) - self.min_id
                building.cap_points = v["buildings_capture"]

                building_dict[gloc] = building
        return building_dict