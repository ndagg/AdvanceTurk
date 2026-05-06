# -*- coding: utf-8 -*-
"""
Created on Sun April 05 15:16:42 2026

@author: ndagg
"""

def gloc_2_loc(gloc: int, dims: tuple[int]) -> tuple[int]:
    loc = (gloc%dims[0], gloc//dims[0])
    return loc

def loc_2_gloc(loc: tuple[int], dims: tuple[int]) -> int:
    gloc = loc[0] + loc[1]*dims[0]
    return gloc

def match_terrain_name(name: str, terrain_types: list[str]) -> int:
    for i, string in enumerate(terrain_types):
        if string in name:
            return i 