# -*- coding: utf-8 -*-
"""
Created on Sun May 25 12:35:37 2025

@author: ndagg
"""
from src.gameObjects.cos import CO

from src.gameUtils.aw_lists import (
    PRIMARY_ATTACK,
    SECONDARY_ATTACK,
    TERRAIN_DEFENCE)

from src.gameObjects.units import ARCHETYPES, UNITS


class Andy(CO):
    
    co_power_cost = 27000
    super_power_cost = 54000
    
    def apply_co_power(self, gamestate):
        """
        Apply all effects of Andy's power to the gameboard
        """
        super.apply_co_power(gamestate)
        for unit in gamestate.players[self.team_number].units:
            unit.hp += 20
            if unit.hp > 100:
                unit.hp = 100
            unit.vhp = (unit.hp + 9) // 10
    
    def apply_super_power(self, gamestate):
        """
        Apply all effects of Andy's super to the gameboard
        """
        super.apply_super_power(gamestate)
        for unit in gamestate.players[self.team_number].units:
            unit.move += 1
            unit.hp += 50
            if unit.hp > 100:
                unit.hp = 100
            unit.vhp = (unit.hp + 9) // 10
            
    def end_co_power(self, gamestate):
        """
        Remove all temporary effects of Andy's power from the gameboard
        """
            
    def end_super_power(self, gamestate):
        """
        Remove all temporary effects of Andy's super from the gameboard
        """
        super.end_super_power(gamestate)
        for unit in gamestate.players[self.team_number].units:
            unit.move = ARCHETYPES[unit.id].move
    
    def attack_calculator(self, a_unit, d_unit, a_terrain):
        """
        Calculate Andy's attack range during a combat
        """
        if a_unit.ammo:
            weapon_attack = PRIMARY_ATTACK[a_unit.id, d_unit.id]
        else:
            weapon_attack = SECONDARY_ATTACK[a_unit.id, d_unit.id]
        
        unit_attack = self.co_attack[a_unit.id]
        if self.co_power_active:
            unit_attack += 10
        elif self.super_power_active:
            unit_attack += 20
            
        attack_high = (
            weapon_attack
            * unit_attack/100
            + self.luck)
        
        attack_low = (
            weapon_attack
            * unit_attack/100
            - self.bad_luck)
        
        return attack_high, attack_low