# -*- coding: utf-8 -*-
"""
Created on Sun May 17 12:35:37 2026

@author: ndagg
"""
from src.gameObjects.cos import CO

from src.gameUtils.aw_lists import (
    PRIMARY_ATTACK,
    SECONDARY_ATTACK,
    TERRAIN_DEFENCE)

from src.gameObjects.units import Unit, ARCHETYPES, UNITS


class Sonja(CO):
    
    co_power_cost = 27000
    super_power_cost = 45000

    def __init__(self, player_number):
        super().__init__(player_number)

        self.bad_luck = -9
    
    def attack_calculator(self, a_unit: Unit, d_unit: Unit, a_terrain: int, counter: bool) -> tuple[int]:
        """
        Calculate the default attack range during a combat
        """
        if a_unit.ammo:
            weapon_attack = PRIMARY_ATTACK[a_unit.id][d_unit.id]
        else:
            weapon_attack = SECONDARY_ATTACK[a_unit.id][d_unit.id]

        unit_attack = self.co_attack[a_unit.id] 
        if counter:
            unit_attack *= 1.5
            
        attack_high = (
            weapon_attack
            * unit_attack/100
            + self.luck)
        
        attack_low = (
            weapon_attack
            * unit_attack/100
            - self.bad_luck)
        
        return attack_high, attack_low