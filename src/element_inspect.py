# -*- coding: utf-8 -*-
"""
Created on Sat May 10 20:33:53 2025

@author: ndagg
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import json

import numpy as np


def get_html():
    driver = webdriver.Firefox()
    
    # Open the webpage
    driver.get('https://awbw.amarriner.com/game.php?games_id=1422829')
    
    # Get the page source (HTML)
    html = driver.page_source
    print(html)
    
    # Always close the driver
    driver.quit()
    
    return html


def get_terrain_dict(html_text):
    start = html_text.index("terrainInfo")
    terrain_info_text = html_text[start+14:].partition(";")[0]
    terrain_dict = json.loads(terrain_info_text)
    return terrain_dict


def get_building_dict(html_text):
    start = html_text.index("buildingsInfo")
    building_info_text = html_text[start+16:].partition(";")[0]
    building_dict = json.loads(building_info_text)
    return building_dict


def read_terrain_dict(tdict):
    dims = [len(tdict)]
    
with open("element.txt", 'r') as file:
    file = file.read()
    
html = BeautifulSoup(file, 'html.parser')

game_container = html.find("div", {"id": "gamecontainer"})
game_header_table = game_container.find("div", {"id": "game-header-table"})
gamemap = game_header_table.find_all("a", href=True)[1]

terrain_dict = get_terrain_dict(html.prettify())
building_dict = get_building_dict(html.prettify())
