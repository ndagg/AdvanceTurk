# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 20:27:07 2026

@author: ndagg
"""
from copy import copy, deepcopy
import logging

from src.gameObjects.actions import Action, Move, EndTurn, Capture, BuildUnit
from src.gameObjects.player import Player
from src.gameObjects.buildings import Building, ComTower, Lab, HQ, Base, Airport, Port
from src.gameObjects.units import UNITS, Unit

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
            buildings_dict: dict[int: Building],
            unit_map: object):
        # Stateful - needs deepcopy
        self.players = players
        self.current_player = players[0]
        self.buildings_dict = buildings_dict
        self.unit_lists = unit_lists
        self.current_actions = []
        self.caps_in_progress = []

        # No state - direct reference
        self.current_player_id = players[0].player_number
        self.unit_map = unit_map

    
    def get_actions(self) -> list[Action]:
        """
        Return the list of available actions for the player
        """
        # Regular moves
        moves = self.get_moves()

        # Captures
        captures = self.get_captures(moves)

        # CO Powers
        powers = self.current_player.co.powers_available()

        # Unit builds
        builds = self.get_builds() 

        actions = moves + captures + powers + builds

        logger.debug(
            f"{len(actions)} available actions: " +
            f"{len(moves)} moves, " +
            f"{len(captures)} captures, " +
            f"{len(builds)} builds"
            )
        
        # End turn
        actions.append(EndTurn())

        self.current_actions = actions
        return self.current_actions
        
    def get_moves(self) -> list[Move]:
        """
        Return the list of available moves for the current player
        """
        moves = []
        friendlies = self.unit_lists[self.current_player_id]
        blocking_units = self.unit_lists[1-self.current_player_id]
        self.unit_map.update_move_graphs(blocking_units)
        for unit in friendlies:
            if unit.active:
                moves.extend(
                    self.unit_map.generate_single_unit_moves(
                        unit, blocking_units, friendlies))
        
        return moves
    
    def get_captures(self, moves: list[Move]) -> list[Capture]:
        """
        Return a list of available captures for the current player
        """
        cap_actions = []
        for m in moves:
            if m.unit.id < 2 and m.attack_target is None:
                dest = m.destination
                if dest in self.buildings_dict.keys():
                    if self.buildings_dict[dest].owner != self.current_player_id:
                        cap_actions.append(Capture(m, self.buildings_dict[dest]))
        return cap_actions
    
    def get_builds(self) -> list[BuildUnit]:
        """
        Return a list of available unit builds for the current player
        """
        # Get dict of available production buildings
        production = {k: v for k, v in self.buildings_dict.items() if v.owner == self.current_player_id}
        for p in self.unit_lists:
            for u in p:
                if u.glocation in production.keys():
                    production.remove(u.glocation)
        
        builds = []
        unit_factory = self.current_player.co.factory_list
        for gloc, v in production.items():
            if type(v) is Base:
                unit_id_range = range(13)
            elif type(v) is Airport:
                unit_id_range = range(13, 18)
            elif type(v) is Port:
                unit_id_range = range(18, 24)

            for i in unit_id_range:
                if unit_factory[i].cost <= self.current_player.funds:
                    builds.append(BuildUnit(gloc, i))
        
        return builds

    def make_action_on_new_state(self, original_action: Action, ind: int) -> object:
        """
        Create a new gamestate and apply the effects of a Move to it
        """
        logger.debug(f"Making move: {original_action} - {original_action._id}")
        new_gamestate = self.make_new_state()
        action = new_gamestate.current_actions[ind]

        
        if type(action) is Move:
            if action.attack_target is not None:
                a_survive, d_survive = new_gamestate.make_attack(action)
                if a_survive:
                    new_gamestate.move_unit(action)
            else:
                new_gamestate.move_unit(action)
        
        elif type(action) is BuildUnit:
            pass  # TODO implement buildunit result
        
        elif type(action) is Capture:
            new_gamestate.make_capture(action)
            
        elif type(action) is EndTurn:
            new_gamestate.current_player_id = 1 - new_gamestate.current_player_id
            new_gamestate.current_player = new_gamestate.players[new_gamestate.current_player_id]
        return new_gamestate
    
    def move_unit(self, move: Move):
        """
        Apply relocating Move to a unit
        """
        move.unit.set_gloc(move.destination, self.unit_map.dims)
        move.unit.reduce_fuel(move.fuel_cost)
        move.unit.active = False
        
        # Check if this is abandonning a capture
        self.check_aborted_capture(move.unit)

    def make_attack(self, move: Move) -> tuple[bool]:
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

        d_survive, delta_value = defender.take_damage(expected)
        logger.debug(f"{defender} survives: {d_survive}")
        defend_co.gain_charge(delta_value)

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
            a_survive, delta_value = attacker.take_damage(expected)
            attack_co.gain_charge(delta_value)
            if not a_survive:
                self.check_aborted_capture(attacker)
                self.unit_lists[attacker.owner].remove(attacker)
        else:
            a_survive = True
            self.check_aborted_capture(defender)
            self.unit_lists[defender.owner].remove(defender)
            
        
        return a_survive, d_survive

    def make_capture(self, capture: Capture):
        """
        Apply the effects of a capture action
        """
        cap_delta = capture.unit.capture_power * capture.unit.vhp
        original_owner = capture.building.owner
        capped = capture.building.capture(cap_delta, self.current_player_id)
        if capped:
            logger.debug(
                f"Capture of {capture.building} from {capture.building.owner} by {capture.unit.owner}"
                )
            if type(capture.building) not in (ComTower, Lab):
                if original_owner is not None:
                    self.players[original_owner].co.num_income_buildings -= 1
                self.current_player.co.num_income_buildings += 1
                if type(capture.building) is HQ:
                    # This attribute will only exist in this circumstance
                    self.hq_cap = capture.building.owner
            elif type(capture.building) is ComTower:
                if original_owner is not None:
                    self.players[original_owner].co.remove_com_tower()
                self.current_player.co.add_com_tower()
        
    def make_build(self, build: BuildUnit):
        """
        Apply the effects of a BuildUnit action
        """
        unit = build.unit()
        unit.owner = self.current_player_id
        unit.set_gloc(build.glocation, self.unit_map.dims)
        unit.active = False
        self.current_player.co.funds -= unit.cost
        ### 
        
    def check_aborted_capture(self, unit: Unit):
        """
        Check whether a move has resulted in a cancelled building capture
        """
        if unit.id < 3:
            try:
                self.buildings_dict[unit.glocation].cap_points = 20
            except KeyError:
                pass
            
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
        for i, p in enumerate(self.unit_lists):
            if not p:
                gameover = True
                logger.info(f"Gameover, player {i} has no units")
        cap = getattr(self, "hq_cap", False)
        if cap:
            gameover = True
            logger.info(f"Gameover, player {cap} has lost their HQ")

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
            "buildings_dict",
            "players", 
            "current_player")}
        new.__dict__.update(deepcopy(dcs))
        return new
