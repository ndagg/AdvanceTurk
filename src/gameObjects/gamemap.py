# -*- coding: utf-8 -*-
"""
Created on Fri May 23 19:48:00 2025

@author: ndagg
"""

import numpy as np
import networkx as nx

from src.gameUtils.aw_lists import (
    TERRAIN_TYPES,
    TERRAIN_COST
    )
from src.gameObjects.moves import Move


class BaseMap():
    """
    A class for representing the basic state of the game map
    """
    def __init__(self, terrain_dict, building_dict):
        # Get map dimensions
        x_dim = max(
            max(int(i) for i in building_dict.keys()),
            max(int(i) for i in terrain_dict.keys())) + 1
        y_dim = max(
            max(int(i) for i in building_dict['0'].keys()),
            max(int(i) for i in terrain_dict['0'].keys())) + 1
        
        self.dims = [x_dim, y_dim]
        self.terrain_arr = np.zeros(self.dims, dtype=int)
        
        self.populate_terrain_array(terrain_dict, building_dict)
                    
        # Generate movement type subgraphs
        self.generate_move_type_graphs()
        
    def populate_terrain_array(self, terrain_dict, building_dict):
        """
        Construct an array containing terrain types from the  dictionaries
        """
        # Traverse terrain dict
        for x in range(self.dims[0]):
            str_x = str(x)
            if str_x in terrain_dict.keys():
                column = terrain_dict[str_x]
            else:
                continue
            for y in range(self.dims[1]):
                str_y = str(y)
                # In instances where there are no buildings in the column
                # the website uses a list instead of a dict
                if type(column) is dict:
                    if str_y in column.keys():
                        string = column[str_y]["terrain_name"]
                    else:
                        continue
                else:
                    string = column[y]["terrain_name"]
                self.terrain_arr[x, y] = self.match_terrain_name(string)
        
        # Traverse building dict
        for x in range(self.dims[0]):
            str_x = str(x)
            if str_x in building_dict.keys():
                column = building_dict[str_x]
            else:
                continue
            for y in range(self.dims[1]):
                str_y = str(y)
                # In instances where there is one building in the column
                # the website uses a list instead of a dict
                if type(column) is dict:
                    if str_y in column.keys():
                        string = column[str_y]["terrain_name"]
                    else:
                        continue
                else:
                    if y >= len(column):
                        continue
                    else:
                        string = column[y]["terrain_name"]
                self.terrain_arr[x, y] = self.match_terrain_name(string)

    def match_terrain_name(self, name):
        for i, string in enumerate(TERRAIN_TYPES):
            if string in name:
                return i 
            
    def generate_move_type_graphs(self):
        """
        Generate a set of graphs for calculating possible moves
        """
        def generate_sub_graph(super_graph, move_type):
            """
            Generate a sub graph for a particular movement type
            """
            costs = TERRAIN_COST[move_type]
            
            nodes = [n for n in super_graph._node if costs[super_graph._node[n]["terrain"]]]
            sub_graph = super_graph.subgraph(nodes).copy()
            
            for e in sub_graph.edges:
                sub_graph.edges[e]["cost"] = costs[sub_graph._node[e[1]]["terrain"]]
            
            return sub_graph
        
        # Create directed graph
        super_graph = nx.DiGraph()
        dims = self.dims
        
        # Create graph of all tiles
        n = 0
        for y in range(dims[1]):
            for x in range(dims[0]):
                super_graph.add_node(
                    n, coords=[x, y], terrain=self.terrain_arr[x, y])
                # Add horizontal edges
                if n > 0 and n % dims[0]:
                    super_graph.add_edge(n-1, n)
                    super_graph.add_edge(n, n-1)
                # Add vertical edges
                if y > 0:
                    super_graph.add_edge(n-dims[0], n)
                    super_graph.add_edge(n, n-dims[0])
                n += 1
        
        # Get sub graphs for each movement type
        self.sub_graphs = []
        for i in range(len(TERRAIN_COST)):
            self.sub_graphs.append(generate_sub_graph(super_graph, i))
        
        self.super_graph = super_graph
                
          
class UnitMap():
    """
    A map class for determining what moves a unit can make
    
    Attributes
    ----------
    super_graph : DiGraph
        The terrain graph for the map
    terrain_graphs : list of DiGraphs
        The list of movement type graphs for the map
    unit_list : list
        The list of units on the map
    dims : list
        The x and y dimensions of the map
    player_unit_lists : dict
        A dictionary keyed by player index, with each value being a list of
        that player's units
    player_move_lists : dict
        A dictionary keyed by player index, with each value being a list of
        that player's available moves
    """
    
    def __init__(self, base_map, unit_list):
        self.super_graph = base_map.super_graph
        self.terrain_graphs = base_map.sub_graphs
        self.unit_list = unit_list
        self.dims = base_map.dims
        
        self.player_unit_lists = {}
        for unit in unit_list:
            if unit.owner not in self.player_unit_lists:
                self.player_unit_lists[unit.owner] = [unit]
            else:
                self.player_unit_lists[unit.owner].append(unit)
            
        self.player_move_lists = {i: [] for i in self.player_unit_lists.keys()}
                
    
    def generate_single_unit_move(self, unit):
        """
        Generate a subgraph showing the possible moves for a unit
        """
        movetype_graph = self.terrain_graphs[unit.move_type]
        # Get movements considering only terrain constraints
        if unit.glocation in movetype_graph:
            no_att, _ = nx.single_source_dijkstra(
                movetype_graph, unit.glocation, cutoff=unit.move, weight='cost')
        # Slightly inelegant way of getting only the current tile
        else:
            return self.super_graph.subgraph([unit.glocation]).copy()
        # Get attackable tiles for direct units
        # TODO - pick which tile to attack from
        if unit.direct:
            att, _ = nx.single_source_dijkstra(
                movetype_graph, unit.glocation, cutoff=unit.move+1, weight='cost')
        # Get attackable tiles for indirect units
        else:
            ...
            # att = super_graph.subgraph
            
        # TODO - remove moves to occupied tiles
        # TODO - remove moves through enemy units
        
        
        no_attack_moves = movetype_graph.subgraph(no_att).copy()
        attack_moves = ...
        return no_attack_moves
    


    def generate_unit_moves(self, player_number):
        for unit in self.player_unit_lists[player_number]:
            self.player_move_lists[player_number].append(
                self.generate_single_unit_move(unit))
            
