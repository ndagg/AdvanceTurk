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

class GameReader:
    """
    A class for fetching and interpreting game data from amarriner.com
    """
    def __init__(self, driver=None):
        if driver is None:
            self.driver = webdriver.Firefox
        else:
            self.driver = driver
    
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
    
    def get_building_dict(self):
        """
        Extract the building dictionary from the game page HTML
        """
        start = self.prettied.index("buildingsInfo")
        building_info_text = self.prettied[start+16:].partition(";")[0]
        building_dict = json.loads(building_info_text)
        self.building_dict = building_dict

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
        self.get_building_dict()
        basemap = BaseMap(self.terrain_dict, self.building_dict)
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
        unit_lists = [[]] * len(self.ids)

        for k, v in self.unit_dict.items():
            owner = int(v["units_players_id"]) - self.min_id
            unit = UNIT_NAMES.index(v["units_name"])
            unit = UNITS[unit]()
            unit.fuel = v["units_fuel"]
            unit.hidden = v["units_sub_dive"] != "N"
            if unit.id not in [0, 2]:  # Inf and Recon has infinite ammo
                unit.ammo = v["units_ammo"]
            unit.set_loc((v["units_X"], v["units_y"]))
            unit.vhp = v["units_hit_points"]
            if unit.vhp < 10:
                unit.hp = unit.vhp * 10 + 5  # Assumes unit is at mid-point of hp bracket
            unit.active = bool(v["units_moved"])
            # TODO - include transports

            unit_lists[owner].append(unit)
        return unit_lists

