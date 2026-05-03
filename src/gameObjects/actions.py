# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 15:52:24 2025

@author: ndagg
"""

from src.gameObjects.buildings import Building
from src.gameObjects.units import Unit

class Action():
    """
    An abstract class covering each of the possible player actions
    to be acted on by decision-making logic
    """
    def __init__(self):
        self._id = hex(id(self))

    def __repr__(self):
        return f"{self.__class__.__name__}"


class Move(Action):
    """
    A class for storing unit moves and attacks
    """
    
    def __init__(self, unit: object, destination: int, fuel: int, attack_target: object=None):
        super().__init__()
        self.unit = unit
        self.destination = destination
        self.fuel_cost = fuel
        self.attack_target = attack_target
    
    def __repr__(self):
        return f"Move(unit: {self.unit.__class__.__name__}, dest: {self.destination}, attack: {self.attack_target})"
    

class EndTurn(Action):
    """
    A class for representing an end turn
    """
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "End turn"


class Capture(Action):
    """
    A class for representing infantry captures
    """
    def __init__(self, move: Move, building: Building):
        super().__init__()
        self.unit = move.unit
        self.fuel_cost = move.fuel_cost
        self.building = building

class COPower(Action):
    """
    A class for representing COPower activations
    """
    def __init__(self):
        super().__init__()
        # TODO
    

class SuperPower(Action):
    """
    A class for representing super-power activations
    """
    def __init__(self):
        super().__init__()
        # TODO


class BuildUnit(Action):
    """
    A class for representing creating new units
    """
    def __init__(self, unit_type: type, tile: int):
        super().__init__()
        # TODO