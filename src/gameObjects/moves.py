# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 15:52:24 2025

@author: ndagg
"""

class Move():
    """
    A class for storing moves to be acted on by decision-making logic
    """
    
    def __init__(self, unit, graph):
        self.unit = unit
        self.graph = graph