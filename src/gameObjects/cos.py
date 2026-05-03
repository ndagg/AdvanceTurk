# -*- coding: utf-8 -*-
"""
Created on Sun May 25 10:05:39 2025

@author: ndagg
"""

from abc import ABC, abstractmethod
import copy
import logging

from src.gameUtils.aw_lists import (
    PRIMARY_ATTACK,
    SECONDARY_ATTACK,
    TERRAIN_DEFENCE)

from src.gameObjects.units import Unit, ARCHETYPES, UNITS
from src.gameObjects.actions import Action, SuperPower, COPower

logger = logging.getLogger("mainlogger.cos")


class CO(ABC):
    
    power_meter = 0
    co_power_cost = 0
    super_power_cost = 0
    
    team_number = 0
    
    funds_per_prop = 1000
    
    co_attack = [100] * 25
    co_defence = [100] * 25
    
    co_power_active = False
    super_power_active = False
    
    luck = 9
    bad_luck = 0
    
    com_towers = 0
    
    funds = 0
    
    def __init__(self):
        self.unit_factory_init()
        
    def unit_factory_init(self):
        """
        Initialise the unit factory by creating a default unit list for the co
        """
        self.factory_list = []
        for unit in UNITS:
            unit = unit(self.team_number)
            self.factory_list.append(unit)
            
    
    def unit_factory(self, unit_id: int) -> Unit:
        """
        Create a unit with the default stats
        """
        new_unit = copy.deepcopy(self.factory_list[unit_id])
            
        # Apply comm tower effects
        new_unit.attack += self.com_towers * 10
        
        return new_unit
    
    def gain_charge(self, amount: int):
        """
        Increase the CO power charge when taking damage
        """
        if self.power_meter < self.super_power_cost:
            self.power_meter += amount
            if self.power_meter > self.super_power_cost:
                self.power_meter = self.super_power_cost

    def powers_available(self) -> list[Action]:
        """
        Return the available CO power actions
        """
        if self.power_meter == self.super_power_cost:
            return [COPower, SuperPower]
        elif self.power_meter >= self.co_power_cost:
            return [COPower]
        return []
    
    def apply_co_power(self, gamestate):
        """
        Apply all default effects of a power to the gameboard
        """
        self.co_power_active = True
        self.power_meter -= self.co_power_cost
        
    def end_co_power(self, gamestate):
        """
        Remove all default temporary effects of a power from the gameboard
        """
        self.co_power_active = False
    
    def apply_super_power(self, gamestate):
        """
        Apply all default effects of a super to the gameboard
        """
        self.super_power_active = True
        self.power_meter = 0
        
    def end_super_power(self, gamestate):
        """
        Remove all default temporary effects of a super from the gameboard
        """
        self.super_power_active = False
        
    def add_com_tower(self, gamestate):
        """
        Apply com tower bonus to all units
        """
        self.co_attack += 10
    
    def remove_com_tower(self, gamestate):
        """
        Remove com tower bonus from all units
        """
        self.co_attack -= 10
    
    def attack_calculator(self, a_unit, d_unit, a_terrain):
        """
        Calculate the default attack range during a combat
        """
        if a_unit.ammo:
            weapon_attack = PRIMARY_ATTACK[a_unit.id][d_unit.id]
        else:
            weapon_attack = SECONDARY_ATTACK[a_unit.id][d_unit.id]
        
        unit_attack = self.co_attack[a_unit.id]
        if self.co_power_active or self.super_power_active:
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

    def defence_calculator(self, a_unit, d_unit, d_terrain):
        """
        Calculate the default defence during a combat
        """
        unit_defence = self.co_defence[d_unit.id]
        if self.co_power_active or self.super_power_active:
            unit_defence += 10
        
        defence = unit_defence + TERRAIN_DEFENCE[d_terrain] * d_unit.vhp
        return defence
    
class BlankCO(CO):
    def __init__(self):
        super().__init__()
        logger.warning("Using BlankCO!")