# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 20:27:07 2026

@author: ndagg
"""

class GameState():

    def __init__(
            self,
            players: list[object],
            gamemap: object):
        self.players = players
        self.current_player = players[0]
        self.gamemap = gamemap

    def get_moves(self):
        ...
    
    def make_move(self):
        ...

    def evaluate(player: object):
        ...
    
    def isGameOver(self):
        ...