# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 15:52:24 2025

@author: ndagg
"""

class Move():
    """
    A class for storing moves to be acted on by decision-making logic
    """
    
    def __init__(self, unit: object, destination: int, fuel: int, attack_target: object=None):
        self.unit = unit
        self.destination = destination
        self.fuel_cost = fuel
        self.attack_target = attack_target
        self._id = hex(id(self))
    
    def __repr__(self):
        return f"Move(unit: {self.unit.__class__.__name__}, dest: {self.destination}, attack: {self.attack_target})"