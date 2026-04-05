# -*- coding: utf-8 -*-
"""
Created on Sat May 10 20:33:53 2025

@author: ndagg
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import json

from src.gameObjects.gamemap import BaseMap

class GameReader:
    """
    A class for fetching and interpreting game data from amarriner.com
    """
    def __init__(self, driver=None):
        if driver == None:
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
    
    def generate_basemap(self):
        """
        Generate the BaseMap object for the currently stored game
        """
        self.get_terrain_dict()
        self.get_building_dict()
        basemap = BaseMap(self.terrain_dict, self.building_dict)
        return basemap
    
    def create_players(self):
        """
        """



