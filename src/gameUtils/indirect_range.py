# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 16:16:44 2025

@author: ndagg
"""
import numpy as np

from src.codeUtils.helpers import gloc_2_loc, loc_2_gloc

def calc_range_mask():
    dist_mask = np.zeros((21, 21), dtype=int)
    for x in range(21):
        for y in range(21):
            dist_mask[x, y] = abs(x - 10) + abs(y - 10)
    return dist_mask

DIST_MASK = calc_range_mask()

def generate_indirect_attack_tiles(glocation: int, min_range: int, max_range: int, dims: tuple) -> list:
    """
    Given a grid location and ranges calculate all grid locations within taxicab distance range
    """
    unit_loc = gloc_2_loc(glocation, dims)
    targs = np.where((DIST_MASK >= min_range) & (DIST_MASK <= max_range))
    # Get tile grid locations in range
    targx = (targs[0] - 10) + unit_loc[0]
    targy = (targs[1] - 10) + unit_loc[1]
    # Exclude out of bounds tiles
    targs = [(int(x), int(y)) for x, y in zip(targx, targy) if x >= 0 and x < dims[0] and y >= 0 and y < dims[1]]
    targs = [loc_2_gloc(i, dims) for i in targs]
    return targs
