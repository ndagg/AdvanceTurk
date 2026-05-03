# -*- coding: utf-8 -*-
"""
Created on Fri May 23 20:47:16 2025

@author: ndagg
"""

class Building():
    def __init__(self, gloc: int):
        self.owner = None
        self.cap_points = 20
        self.gloc = gloc
        
    def capture(self, cap_delta: int, player_id: int) -> bool:
        self.cap_points -= cap_delta
        if self.cap_points <= 0:
            self.owner = player_id
            return True
        else:
            return False
    
class Production(Building):
    def __init__(self, gloc: int):
        super().__init__(gloc)
        self.available = True

class Base(Production):
    pass

class Airport(Production):
    pass

class Port(Production):
    pass

class City(Building):
    pass

class HQ(Building):
    pass

class ComTower(Building):
    pass

class Lab(Building):
    pass