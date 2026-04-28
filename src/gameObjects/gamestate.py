# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 20:27:07 2026

@author: ndagg
"""
from copy import deepcopy
import logging

from src.gameObjects.moves import Move
from src.gameUtils.damage_calc import calc_damage

logger = logging.getLogger("mainlogger.gamestate")

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
        """
        Return the list of available moves for the current player
        """
        self.current_moves = []
        for unit in self.current_player.units:
            if unit.active:
                self.current_moves.extend(
                    self.unit_map.generate_single_unit_moves(unit))
        return self.current_moves

    def make_move_on_new_state(self, original_move: object, ind: int) -> object:
        """
        Create a new gamestate and apply the effects of a Move to it
        """
        logger.debug(f"Making move: {original_move} - {original_move._id}")
        new_gamestate = deepcopy(self)
        move = new_gamestate.current_moves[ind]
        logger.debug(f"Copied move: {move} - {move._id}")

        if move.attack_target is not None:
            a_survive, d_survive = self.make_attack(move)
            if a_survive:
                self.unit_map.move_unit(move)
        else:
            self.unit_map.move_unit(move)
        return new_gamestate
    
    def make_attack(self, move: object) -> tuple[bool]:
        """
        Apply the effects of an attack to the two units involved
        """
        attacker = move.unit
        defender = move.attack_target
        attack_co = self.players[attacker.owner].co
        defend_co = self.players[defender.owner].co
        attack_terrain = self.unit_map.super_graph._node[attacker.glocation]['terrain']
        defend_terrain = self.unit_map.super_graph._node[defender.glocation]['terrain']

        # TODO - consider random variance, and fucking Sonja
        hi, lo = calc_damage(
            attacker,
            defender,
            attack_terrain,
            defend_terrain,
            attack_co,
            defend_co
            )
        expected = (hi+lo)//2
        d_survive = defender.take_damage(expected)

        if d_survive and attacker.direct:
            hi, lo = calc_damage(
                defender,
                attacker,
                defend_terrain,
                attack_terrain,
                defend_co,
                attack_co
                )
            expected = (hi+lo)//2
            a_survive = attacker.take_damage(expected)
            if not a_survive:
                self.players[attacker.owner].units.remove(attacker)
        else:
            self.players[defender.owner].units.remove(defender)
        
        return a_survive, d_survive

    def evaluate(self, evaluator: object) -> int:
        """
        Determine the value of the current player's position
        """
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
