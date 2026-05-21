# -*- coding: utf-8 -*-
"""
Created on Sun May 25 12:36:55 2025

@author: ndagg
"""
from src.gameObjects.cos import CO

from src.gameUtils.aw_lists import (
    PRIMARY_ATTACK,
    SECONDARY_ATTACK,
    TERRAIN_DEFENCE)

from src.gameObjects.units import ARCHETYPES, UNITS
            

class Sami(CO):
    
    co_power_cost = 27000
    super_power_cost = 72000
    
    def unit_factory_init(self):
        """
        Create units with Sami's stats
        """
        self.factory_list = []
        for unit in UNITS:
            unit = unit(self.team_number)
            
            # Apply weapon damage
            if unit.weapon is not None:
                unit.weapon.set_attack[unit.id]
            if unit.secondary_weapon is not None:
                unit.secondary_weapon.set_attack[unit.id]
        
        if unit.id in [0, 1]:
            unit.capture_power = 1.5
        elif unit.transport is not None:
            unit.move += 1
            
        self.factory_list.append(unit)
                
    def apply_co_power(self, gamestate):
        """
        Apply all effects of Sami's power to the gameboard
        """
        super.apply_co_power(gamestate)
        for unit in gamestate.players[self.team_number].units:
            if unit.id in [0, 1]:
                unit.move += 1

    def end_co_power(self, gamestate):
        """
        Remove all temporary effects of Sami's power from the gameboard
        """
        super.end_co_power(gamestate)
        for unit in gamestate.players[self.team_number].units:
            if unit.id in [0, 1]:
                unit.move = ARCHETYPES[unit.id].move
                
    def apply_super_power(self, gamestate):
        """
        Apply all default effects of a super to the gameboard
        """
        super.apply_super_power(gamestate)
        for unit in gamestate.players[self.team_number].units:
            if unit.id in [0, 1]:
                unit.move += 2
                unit.capture_power = 20
        
    def end_super_power(self, gamestate):
        """
        Remove all default temporary effects of a super from the gameboard
        """
        super.end_super_power(gamestate)
        for unit in gamestate.players[self.team_number].units:
            if unit.id in [0, 1]:
                unit.move = ARCHETYPES[unit.id].move
                unit.capture_power = 1.5
                
    def attack_calculator(self, a_unit, d_unit, a_terrain):
        """
        Calculate Sami's attack range during a combat
        """
        if a_unit.ammo:
            weapon_attack = PRIMARY_ATTACK[a_unit.id, d_unit.id]
        else:
            weapon_attack = SECONDARY_ATTACK[a_unit.id, d_unit.id]
        
        unit_attack = self.co_attack[a_unit.id]
        if self.co_power_active:
            if a_unit.id in [0, 1]:
                unit_attack += 60
            else:
                unit_attack += 10
        
        if self.super_power_active:
            if a_unit.id in [0, 1]:
                unit_attack += 70
            else:
                unit_attack += 10
            
        attack_high = (
            weapon_attack
            * unit_attack/100
            + self.luck)
        
        attack_low = (
            weapon_attack
            * unit_attack/100
            - self.bad_luck)
        
        return attack_high, attack_low