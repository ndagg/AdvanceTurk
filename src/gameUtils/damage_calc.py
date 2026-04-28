# -*- coding: utf-8 -*-
"""
Created on Tue May 20 17:27:30 2025

@author: ndagg
"""

def calc_damage(
        a_unit: object, 
        d_unit: object,
        a_terrain: int, 
        d_terrain: int,
        a_co: object, 
        d_co: object,
        ) -> list[int]:
    """
    Calculate the damage dealt range of an attack
    """
    # Get attack and defence values from COs
    attack_high, attack_low = a_co.attack_calculator(a_unit=a_unit, d_unit=d_unit, a_terrain=a_terrain)
    unit_defence = d_co.defence_calculator(a_unit, d_unit, d_terrain)

    damage_high = (
        attack_high
        * a_unit.vhp
        * (200 - unit_defence * d_unit.vhp)/100)

    damage_low = (
        attack_low
        * a_unit.vhp
        * (200 - unit_defence * d_unit.vhp)/100)

    a_range = [damage_low, damage_high]
    return a_range