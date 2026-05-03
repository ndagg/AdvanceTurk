# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 20:27:07 2026

@author: ndagg
"""
from copy import copy, deepcopy
import logging

from src.gameObjects.actions import Action, Move, EndTurn, Capture
from src.gameObjects.player import Player
from src.gameUtils.damage_calc import calc_damage

logger = logging.getLogger("mainlogger.gamestate")

class GameState():
    """
    A class for carrying the required state for a single moment in a game
    """
    def __init__(
            self,
            players: list[Player],
            unit_lists: list[list],
            unit_map: object):
        # Stateful - needs deepcopy
        self.players = players
        self.current_player = players[0]
        self.unit_lists = unit_lists
        self.current_actions = []

        # No state - direct reference
        self.current_player_id = players[0].player_number
        self.unit_map = unit_map

    
    def get_actions(self) -> list[Action]:
        """
        Return the list of available actions for the player
        """
        # Regular moves
        self.current_actions = self.get_moves()

        # Captures

        # CO Powers
        self.current_actions.extend(
            self.current_player.co.powers_available())
        
        # End turn
        self.current_actions.append(EndTurn())
        

    def get_moves(self) -> list[Move]:
        """
        Return the list of available moves for the current player
        """
        self.current_actions = []
        friendlies = self.unit_lists[self.current_player_id]
        blocking_units = self.unit_lists[1-self.current_player_id]
        self.unit_map.update_move_graphs(blocking_units)
        for unit in friendlies:
            if unit.active:
                self.current_actions.extend(
                    self.unit_map.generate_single_unit_moves(
                        unit, blocking_units, friendlies))
        
        return self.current_actions
    
    def get_captures(self, moves: list[Move]) -> list[Capture]:
        """
        Return a list of available captures for the current player
        """
        cap_moves = []
        for m in moves:
            if m.unit.id < 2 and m.attack_target is None:
                if m.destination:
                    pass

    def make_move_on_new_state(self, original_move: object, ind: int) -> object:
        """
        Create a new gamestate and apply the effects of a Move to it
        """
        logger.debug(f"Making move: {original_move} - {original_move._id}")
        new_gamestate = self.make_new_state()
        move = new_gamestate.current_moves[ind]

        if type(move) is EndTurn:
            new_gamestate.current_player = 1 - new_gamestate.current_player
            return new_gamestate

        if move.attack_target is not None:
            a_survive, d_survive = new_gamestate.make_attack(move)
            if a_survive:
                new_gamestate.move_unit(move)
        else:
            new_gamestate.move_unit(move)
        return new_gamestate
    
    def move_unit(self, move: object):
        """
        Apply relocating (no attack) Move to a unit
        """
        move.unit.set_gloc(move.destination, self.unit_map.dims)
        move.unit.reduce_fuel(move.fuel_cost)
        move.unit.active = False
    
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
        logger.debug(f"{attacker} damages {defender} for {expected} damage")

        d_survive = defender.take_damage(expected)
        logger.debug(f"{defender} survives: {d_survive}")

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
                self.unit_lists[attacker.owner].remove(attacker)
        else:
            a_survive = True
            self.unit_lists[defender.owner].remove(defender)
        
        return a_survive, d_survive

    def evaluate(self, evaluator: object) -> int:
        """
        Determine the value of the current player's position
        """
        value = self.current_player.evaluate()  # TODO - work out how to handle evaluators
        return value

    def is_gameover(self):
        """
        Check to see whether the game is over based on the gamestate
        """
        gameover = False
        for p in self.unit_lists:
            if not p:  # TODO - include check for HQ/lab capture
                gameover = True
        return gameover
    
    def make_new_state(self) -> object:
        """
        Duplicate the current gamestate, deepcopying required attributes
        """
        cls = self.__class__
        new = cls.__new__(cls)
        # Direct references
        new.current_player_id = self.current_player_id
        new.unit_map = self.unit_map
        # Deep copies - done as single dict so that units in actions and lists match
        dcs = {k:self.__dict__[k] for k in (
            "current_actions", 
            "unit_lists", 
            "players", 
            "current_player")}
        new.__dict__.update(deepcopy(dcs))
        return new

