# -*- coding: utf-8 -*-
"""
Created on Sun April 05 17:08:42 2026

@author: ndagg
"""
import networkx as nx
import logging

from src.gameUtils.indirect_range import get_indirect_attack_tiles
from src.gameUtils.aw_lists import ANY_ATTACK

from src.gameObjects.moves import Move

logger = logging.getLogger("mainlogger.unitmap")

class UnitMap():
    """
    A map class for determining what moves a unit can make
    
    Attributes
    ----------
    super_graph : DiGraph
        The terrain graph for the map
    friendly_units : list
        The list of friendly units to consider when calculating moves
    pure_terrain_graphs : list of DiGraphs
        The list of movement type graphs for the map
    dims : list
        The x and y dimensions of the map
    """

    def __init__(self, base_map: object, players: list[object]):
        self.super_graph = base_map.super_graph
        self.pure_terrain_graphs = base_map.sub_graphs
        self.dims = base_map.dims
        self.unit_lists = [i.units for i in players]
        self.terrain_graphs = []

        # TODO - add capture, load, hide, and delete moves
    
    def set_current_player(self, player: object):
        """
        Set state of unit lists used for blocking/targets
        """
        logger.info(f"Current player is: {player.team}, {player.co}")
        self.current_player = player.team
        blocking = list(range(len(self.unit_lists)))
        blocking.remove(player.team)
        blocking_units = []
        [blocking_units.extend(self.unit_lists[d]) for d in blocking]
        self.blocking = blocking_units  # Will need updating if more than two teams are used
        self.targets = blocking_units

    def update_move_graphs(self):
        """
        Update the movement graphs to account for occupied tiles
        """
        self.terrain_graphs = []
        for graph in self.pure_terrain_graphs:
            g = graph.copy()
            for unit in self.blocking:
                if unit.glocation in g:
                    g.remove_node(unit.glocation)
            self.terrain_graphs.append(g)

    def update_units_by_player(self, player: object):
        """
        Update a list of units and update the movement graphs accordingly
        """
        self.unit_lists[player.team] = player.units  # TODO - is this necessary? Can it just pass around a single persistent dict between the player and the unit map
        self.update_move_graphs()

    def generate_single_unit_moves(self, unit: object) -> tuple[list, list]:
        """
        Generate a subgraph showing the possible moves for a unit
        """
        #
        # This Function could do with reworking, it's overly complex and probably has too much responsibility
        #

        movetype_graph = self.terrain_graphs[unit.move_type]
        # Get movements considering terrain constraints and other units
        if unit.glocation in movetype_graph:
            no_att, _ = nx.single_source_dijkstra(
                movetype_graph, unit.glocation, cutoff=unit.move, weight='cost')

            for i in self.unit_lists[unit.owner]:
                if i.glocation in no_att and i is not unit:
                    no_att.pop(i.glocation)

            no_att = [Move(unit, dest, cost) for dest, cost in no_att.items() if cost <= unit.fuel]
            
        else:  # Case for unit which is on impassable tile
            no_att = [Move(unit, unit.glocation, 0)]
        # Get attackable tiles for direct units, this could be a lot more efficient
        att = []
        if unit.direct:
            for eunit in self.targets:
                if not ANY_ATTACK[unit.id, eunit.id]:
                    continue  # skip if unit can't attack this type
                for t in no_att:
                    attacks = self.super_graph.neighbors(t.destination)
                    for a in attacks:
                        if a == eunit.glocation:
                            att.append(Move(unit, t.destination, t.fuel_cost, eunit))
        # Get attackable tiles for indirect units
        else:
            att_tiles = self.generate_indirect_attack_tiles(unit.glocation, unit.min_range, unit.max_range, self.dims)
            for t in att_tiles:
                for eunit in self.targets:
                    if not ANY_ATTACK[unit.id, eunit.id]:
                        continue  # skip if unit can't attack this type
                    if t == eunit.glocation:
                        att.append(Move(unit, unit.gloc, 0, eunit))
                        break
        return no_att + att
   
    def generate_indirect_attack_tiles(
            self,
            glocation: int, 
            min_range: int, 
            max_range: int, 
            dims: tuple[int]) -> list:
        return get_indirect_attack_tiles(glocation, min_range, max_range, dims)
    
    def move_unit(self, move: Move):
        start = move.unit.glocation
        move.unit.set_gloc(move.destination, self.dims)
        move.unit.reduce_fuel(move.fuel_cost)
        move.unit.active = False
        