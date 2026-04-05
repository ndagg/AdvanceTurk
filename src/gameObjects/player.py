# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:58:43 2025

@author: ndagg
"""
from src.gameObjects.unitmap import UnitMap

class Player:
    def __init__(self, team_number, co, units, basemap):
        self.team = team_number
        self.co = co
        # self.units = [co.unit_factory(unit) for unit in units]
        self.units = {i:unit for i, unit in enumerate(units)}
        self.unit_map = UnitMap(basemap, units)
        self.moves = {}
        self.attacks = {}

    def generate_unit_moves(self):
        for i, unit in self.units.items():
            self.generate_single_unit_move(unit, i)
    
    def generate_single_unit_move(self, unit, unit_ind):
        moves, attacks = self.unit_map.generate_single_unit_move(unit)
        self.moves[unit_ind] = moves
        self.attacks[unit_ind] = attacks