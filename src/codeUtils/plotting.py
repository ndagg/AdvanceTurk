# -*- coding: utf-8 -*-
"""
Created on Sun May 25 18:58:07 2025

@author: ndagg
"""

import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

from src.gameUtils.aw_lists import TERRAIN_TYPES

from src.codeUtils.constants import TILEPX, TILEHF
from src.codeUtils.helpers import gloc_2_loc, loc_2_gloc

from src.gameObjects.moves import Move


def alpha_blend(foreground, background):
    fore_rgb = foreground[...,:3]
    back_rgb = background[...,:3]
    
    # Extract the alpha channels and normalise to range 0..1
    fore_alpha = foreground[...,3]/255.0
    back_alpha = background[...,3]/255.0
    
    # Work out resultant alpha channel
    outA = fore_alpha + back_alpha*(1-fore_alpha)
    
    # Work out resultant RGB
    outRGB = (
        fore_rgb*fore_alpha[...,np.newaxis]
        + back_rgb*back_alpha[...,np.newaxis]
        *(1-fore_alpha[...,np.newaxis])) / outA[...,np.newaxis]
    
    # Merge RGB and alpha (scaled back up to 0..255) back into single image
    outRGBA = np.dstack((outRGB, outA*255)).astype(np.uint8)
    return outRGBA


def get_pixel_pos(pos):
    return {
        k: [v[0]*TILEPX + TILEHF, v[1]*TILEPX + TILEHF]
        for k, v in pos.items()}


def plot_map_graph(graph, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    
    pos = {k: v["coords"] for k, v in graph._node.items()}
    pos = get_pixel_pos(pos)
    nx.draw(
        graph, pos, ax, node_size=400, node_shape='s',
        node_color='cyan', alpha=0.5)
    
    return ax

def plot_moves(gamestate, unit, dims, ax=None, over_img=True):
    if ax is None:
        fig, ax = plt.subplots()
    
    moves = [move for move in gamestate.current_moves if type(move) is Move and move.unit == unit ]
    pos = [gloc_2_loc(move.destination, dims) for move in moves]
    
    if over_img:
        img = [i for i in ax._children
               if type(i) is matplotlib.image.AxesImage][0]
        ys = [i[0] * TILEPX for i in pos]
        xs = [i[1] * TILEPX for i in pos]
        
        blue = np.array(Image.open("images/highlights.png"))
        
        for x, y in zip(xs, ys):
            img._A[x: x+TILEPX, y: y+TILEPX] = alpha_blend(
                blue, img._A[x: x+TILEPX, y: y+TILEPX])
        
        ax.imshow(img._A)
        
    else:
        pos = get_pixel_pos(pos)
        x = [i[0] for i in pos]
        y = [i[1] for i in pos]
        ax.scatter(x, y, marker='s', s=400, color='cyan', alpha=0.5)
    return ax
    

def add_edge_labels(graph, ax, key):
    pos = {k: v["coords"] for k, v in graph._node.items()}
    pos = get_pixel_pos(pos)
    # labels = {}
    # for e in graph.edges:
    #     labels[e] = graph.edges[e][key]
    labels = {e: graph.edges[e][key] for e in graph.edges}
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels=labels, ax=ax, label_pos=0.3,
        bbox={"ec":(0,0,0,0), "fc":(0,0,0,0)})
    
    return ax
    
    
def plot_map_image(base_map, ax=None):
    sprites = Image.open("images/spritesheet_buildings.png")
    sprites = np.array(sprites)
    
    img_list = []
    height = TILEPX
    start = 0
    end = TILEPX
    for i, t in enumerate(TERRAIN_TYPES):
        img_list.append(sprites[start:end, :, :])
        start += height
        if t == "Silo":
            height = 20
        end += height
        
    img_dims = np.array(base_map.dims + [3])
    img_dims[:2] *= TILEPX
    
    img = np.tile(img_list[0], base_map.dims[::-1] + [1])
    
    for x, col in enumerate(base_map.terrain_arr):
        x *= TILEPX
        for y, terrain in enumerate(col):
            y *= TILEPX
            h = img_list[terrain].shape[0]
            if h == 20:
                y -= 4
                if y == -4:
                    img[0: TILEPX, x: x+TILEPX] = alpha_blend(
                        img_list[terrain][4:], img[0: TILEPX, x: x+TILEPX])
                    continue
            img[y: y+h, x: x+TILEPX] = alpha_blend(
                img_list[terrain], img[y: y+h, x: x+TILEPX])
    
    if ax is None:
        fig, ax = plt.subplots()
    ax.imshow(img)
    
    return ax
    
    
def plot_units_on_map(units, ax):
    pass