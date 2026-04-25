# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 20:27:07 2026

@author: ndagg
"""
from copy import deepcopy

from src.gameObjects.moves import Move
from src.gameUtils.damage_calc import calc_damage


class GameState():

    def __init__(
            self,
            players: list[object],
            unit_map: object):
        self.players = players
        self.current_player = players[0]
        self.unit_map = unit_map
        self.current_moves = []

    def get_moves(self):
        self.current_moves = []
        for i, unit in enumerate(self.current_player.units):
            if unit.active:
                self.current_moves.extend(
                    self.unit_map.generate_single_unit_moves(unit))

    def make_move(self, move: object) -> object:
        if move.attack is not None:
            self.make_attack(move)
        self.unitmap.move_unit(move)
        self.current_moves = [
            m for m in self.current_moves if m.unit != move.unit and m.destination != move.destination]
        return deepcopy(self)
    
    def make_attack(self, move: object):
        """
        Apply the effects of an attack to the two units involved
        """
        attacker = move.unit
        defender = move.attack_target
        # TODO - consider random variance, and fucking Sonja
        hi, lo = calc_damage(
            attacker,
            defender,
            # terrain, COs
            )
        expected = (hi+lo)//2
        d_survive = defender.take_damage(expected)
        if d_survive and attacker.direct:
            hi, lo = calc_damage(
                attacker,
                defender,
                # terrain, COs
            )
            expected = (hi+lo)//2
            a_survive = attacker.take_damage(expected)
        else:
            self.players[defender.owner].units.remove(defender)


    def evaluate(self, evaluator: object) -> int:
        value = evaluator.evaluate(self.current_player)
        return value

    def is_gameover(self):
        """
        Check to see whether the game is over based on the gamestate
        """
        gameover = False
        for p in self.players:
            if not p.units:  # TODO - include check for HQ/lab capture
                gameover = True
        return gameover
