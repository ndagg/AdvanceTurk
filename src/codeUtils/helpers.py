# -*- coding: utf-8 -*-
"""
Created on Sun April 05 15:16:42 2026

@author: ndagg
"""

def gloc_2_loc(gloc, dims):
    loc = (gloc%dims[0], gloc//dims[0])
    return loc

def loc_2_gloc(loc, dims):
    gloc = loc[0] + loc[1]*dims[0]
    return gloc
