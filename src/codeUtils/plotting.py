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

from src.gameObjects.actions import Move
from src.gameObjects.units import UNITS


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


def get_pixel_pos(pos):  # TODO - WTF is going on with this?
    if type(pos) is dict:
        return {
            k: [v[0]*TILEPX + TILEHF, v[1]*TILEPX + TILEHF]
            for k, v in pos.items()}
    else:
        return pos[0]*TILEPX + TILEHF, pos[1]*TILEPX + TILEHF
            


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
    
    moves = [move for move in gamestate.current_actions if type(move) is Move and move.unit == unit ]
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
        # Remove old ax child so that the ax can be further built on
        ax._children = [ax._children[-1]]
        
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
    
    
def plot_map_image(base_map, building_dict, ax=None):
    sprites = Image.open("images/spritesheet_buildings.png")
    sprites = np.array(sprites)
    
    # Set up base image and sprites
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

    # Prepare building dict and coloured buildings
    img_list_red = []
    img_list_blue = []
    for i in img_list:
        # Do not modify initial img_list
        k = i + 0
        j = i + 0
        k[:, :, [1,2]] //=2
        j[:, :, [0,1]] //=2
        k[:, :, [1,2]] += 20
        j[:, :, [0,1]] += 20
        img_list_red.append(k)
        img_list_blue.append(j)
    
    for x_val, col in enumerate(base_map.terrain_arr):
        x = x_val * TILEPX
        for y_val, terrain in enumerate(col):
            y = y_val * TILEPX
            terrain_img = img_list[terrain]
            h = terrain_img.shape[0]
            location = loc_2_gloc((x_val, y_val), base_map.dims)
            if location in building_dict and building_dict[location].owner is not None:
                team = building_dict[location].owner
                if team:
                    terrain_img = img_list_blue[terrain]
                else:
                    terrain_img = img_list_red[terrain]
            if h == 20:
                y -= 4
                if y == -4:
                    img[0: TILEPX, x: x+TILEPX] = alpha_blend(
                        terrain_img[4:], img[0: TILEPX, x: x+TILEPX])
                    continue
            img[y: y+h, x: x+TILEPX] = alpha_blend(
                terrain_img, img[y: y+h, x: x+TILEPX])
    
    if ax is None:
        fig, ax = plt.subplots()
    ax.imshow(img)
    
    return ax
    
    
def plot_units_on_map(units, ax):
    sprites = Image.open("images/spritesheet_units.png")
    sprites = np.array(sprites)

    img_list = []
    height = TILEPX
    start = 0
    end = TILEPX
    for i, t in enumerate(UNITS):
        img_list.append(sprites[start:end, :, :])
        start += height
        end += height

    to_draw = [[img_list[i.id], i.location, i.owner] for i in units]

    img = [i for i in ax._children
            if type(i) is matplotlib.image.AxesImage][0]
    
    for i in to_draw:
        if i[2] == 1:
            i[0] = i[0][:, :, [2, 1, 0, 3]]
        x, y = i[1][1] * TILEPX, i[1][0] * TILEPX
        img._A[x: x+TILEPX, y: y+TILEPX] = alpha_blend(
                i[0], img._A[x: x+TILEPX, y: y+TILEPX])
    
    ax.imshow(img._A)
    return ax