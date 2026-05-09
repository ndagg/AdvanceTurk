# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:58:43 2025

@author: ndagg
"""
from src.gameObjects.cos import BlankCO

class Player:
    def __init__(
            self, player_number: int,
            team_number: int=None, 
            co: object=None):
        self.player_number = player_number
        self.team = team_number
        if co is None:
            self.co = BlankCO(player_number)
        else:
            self.co = co

    def __repr__(self):
        return f"Player {self.player_number} - {id(self)}"