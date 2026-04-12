# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 20:27:07 2026

@author: ndagg
"""

class GameState():

    def __init__(
            self,
            players: list[object],
            unit_map: object):
        self.players = players
        self.current_player = players[0]
        self.unit_map = unit_map

    def get_moves(self):
        moves = []
        for i, unit in self.current_player.units.items():
            moves.extend(self.generate_single_unit_move(unit, i))
        return moves
    
    def generate_single_unit_move(self, unit, unit_ind):
        moves, attacks = self.unit_map.generate_single_unit_move(unit)
        moves[unit_ind] = moves
        attacks[unit_ind] = attacks
        return moves + attacks
    
    def make_move(self, move: tuple):
        if type(move[1]) is tuple:
            self.make_attack(move)
        else:
            self.unitmap.move_unit(move)  # TODO - implement this


    def evaluate(player: object, evaluator: object):
        ...
    
    def is_gameover(self):
        """
        Check to see whether the game is over based on the gamestate
        """
        gameover = False
        for p in self.players:
            if not p.units:  # TODO - include check for HQ/lab capture
                gameover = True
        return gameover