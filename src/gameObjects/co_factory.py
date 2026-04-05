# -*- coding: utf-8 -*-
"""
Created on Mon May 26 13:05:11 2025

@author: ndagg
"""

class COFactory:
    
    def __init__(self, team_number, co):
        self.team_number = team_number
        self.unit_modifier_functions = co.unit_modifier_functions
    
    def create_unit(self, unit):
        # Apply attack lists to unit weapon
        new_unit = unit(self.team_number)
        if new_unit.weapon is not None:
            new_unit.weapon.set_attack[new_unit.id]
        
        if new_unit.secondary_weapon is not None:
            new_unit.secondary_weapon.set_attack[new_unit.id]
            
        for f in self.unit_modifier_functions:
            unit = f(unit)