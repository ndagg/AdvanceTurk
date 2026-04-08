# -*- coding: utf-8 -*-
"""
Created on Sun April 05 17:08:42 2026

@author: ndagg
"""
import networkx as nx

from src.gameUtils.indirect_range import generate_indirect_attack_tiles
from src.gameUtils.aw_lists import ANY_ATTACK


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

    def __init__(self, base_map, unit_dict: dict):
        self.super_graph = base_map.super_graph
        self.pure_terrain_graphs = base_map.sub_graphs
        self.dims = base_map.dims
        self.friendly_units = unit_dict
        self.enemy_units = {}

        # TODO - add capture, load, hide, and delete moves

    def update_move_graphs(self):
        """
        Update the movement graphs to account for occupied tiles
        """
        self.terrain_graphs = []
        for graph in self.pure_terrain_graphs:
            g = graph.copy()
            for unit in self.enemy_units.values():
                if unit.glocation in g:
                    g.remove_node(unit.glocation)
            self.terrain_graphs.append(g)

    def update_enemy_units(self, enemy_units: dict):
        """
        Update the list of enemy units and update the movement graphs accordingly
        """
        self.enemy_units = enemy_units
        self.update_move_graphs()

    def generate_single_unit_move(self, unit: object) -> tuple[list, list]:
        """
        Generate a subgraph showing the possible moves for a unit
        """
        movetype_graph = self.terrain_graphs[unit.move_type]
        # Get movements considering terrain constraints and other units
        # TODO - account for units starting on impassable tiles
        if unit.glocation in movetype_graph:
            no_att, _ = nx.single_source_dijkstra(
                movetype_graph, unit.glocation, cutoff=unit.move, weight='cost')
            no_att = list(no_att.keys())

            for i in self.friendly_units:
                if i.glocation in no_att and i is not unit:
                    no_att.remove(i.glocation)
        else:
            no_att = unit.glocation
        # Get attackable tiles for direct units
        if unit.direct:
            att_tiles = self.generate_direct_attack_tiles(no_att)
        # Get attackable tiles for indirect units
        else:
            att_tiles = generate_indirect_attack_tiles(unit.glocation, unit.min_range, unit.max_range, self.dims)
            # att = super_graph.subgraph
        att = []
        for t in att_tiles:
            for eunit_ind, eunit in self.enemy_units.items():
                if not ANY_ATTACK[unit.id, eunit.id]:
                    continue  # skip if unit can't attack this type
                if t == eunit.glocation:
                    att.append((t, eunit_ind))
                    break

        # unit.moves = movetype_graph.subgraph(no_att).copy()
        # unit.attacks = movetype_graph.subgraph(att).copy()
        # return unit.moves, unit.attacks

        return no_att, att

    def generate_direct_attack_tiles(self, moveable_tiles: list) -> list:
        """
        Get attackable tiles for direct units given a list of moveable tiles
        """
        att = set()
        for tile in moveable_tiles:
            if tile in self.super_graph:
                att.update(self.super_graph.neighbors(tile))
        return list(att)
