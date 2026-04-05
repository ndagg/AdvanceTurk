# -*- coding: utf-8 -*-
"""
Created on Fri May 23 20:47:16 2025

@author: ndagg
"""

from abc import ABC

class Building(ABC):
    def __init__(self):
        self.owner = 0
        self.location = [0, 0]
        self.cap_points = 20
        
    def capture(self, cap_delta):
        self.cap_points -= cap_delta
        if self.cap_points <= 0:
            return True
        else:
            return False
    
class Production(Building):
    def __init__(self):
        super().__init__(self)
        self.available = True

class Base(Production):
    def __init__(self):
        super().__init__(self)
    