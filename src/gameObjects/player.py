# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:58:43 2025

@author: ndagg
"""
from src.gameObjects.unitmap import UnitMap

class Player:
    def __init__(self, team_number, co, units):
        self.team = team_number
        self.co = co
        # self.units = [co.unit_factory(unit) for unit in units]
        self.units = {i:unit for i, unit in enumerate(units)}
        self.moves = {}
        self.attacks = {}