# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:58:43 2025

@author: ndagg
"""

class Player:
    def __init__(self, team_number, co, units, unit_locations):
        self.team = team_number
        self.co = co
        self.units = [co.unit_factory(unit) for unit in units]