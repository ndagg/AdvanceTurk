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

from src.codeUtils.helpers import match_terrain_name

class BaseMap():
    """
    A class for representing the basic state of the game map
    """
    def __init__(
            self, 
            awbw_terrain_dict: dict, 
            awbw_building_dict: dict
            ):
        # Get map dimensions
        x_dim = max(
            max(int(i) for i in awbw_building_dict.keys()),
            max(int(i) for i in awbw_terrain_dict.keys())) + 1
        y_dim = max(
            max(int(i) for i in awbw_building_dict['0'].keys()),
            max(int(i) for i in awbw_terrain_dict['0'].keys())) + 1
        
        self.dims = [x_dim, y_dim]
        self.terrain_arr = np.zeros(self.dims, dtype=int)
        
        self.populate_terrain_array(awbw_terrain_dict, awbw_building_dict)
                    
        # Generate movement type subgraphs
        self.super_graph, self.sub_graphs= self.generate_move_type_graphs()

        # Generate buildings list
        # self.buildings_dict = self.generate_buildings_dict(awbw_building_dict)
        

    def populate_terrain_array(self, terrain_dict: dict, building_dict: dict):
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
                self.terrain_arr[x, y] = match_terrain_name(string, TERRAIN_TYPES)
        
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
                self.terrain_arr[x, y] = match_terrain_name(string, TERRAIN_TYPES)

            
    def generate_move_type_graphs(self) -> tuple[nx.DiGraph, list[nx.DiGraph]]:
        """
        Generate a set of graphs for calculating possible moves
        """
        def generate_sub_graph(super_graph: nx.DiGraph, move_type: int) -> nx.DiGraph:
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
        sub_graphs = []
        for i in range(len(TERRAIN_COST)):
            sub_graphs.append(generate_sub_graph(super_graph, i))
        
        return super_graph, sub_graphs
                
