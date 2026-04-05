# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 16:16:44 2025

@author: ndagg
"""


def get_indirect_tiles(glocation, min_range, max_range, dims):
    """
    Given a grid location and ranges calculate all  grid locations within range
    """
    targs = []
    for x in range(-max_range, max_range):
        for y in range(-max_range, max_range):
            targs = glocation + x + y * dims[0]
    
    def get_taxicab(glocation, targ):
        tc = 