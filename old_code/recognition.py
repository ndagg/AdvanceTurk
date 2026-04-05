# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 19:13:23 2025

@author: ndagg
"""

from PIL import Image

import matplotlib.pyplot as plt
from bisect import bisect

import cv2 as cv
import numpy as np

from screenshot import Screenshotter


def find_pboxes(img):
    
    # Prepare image template
    pbox = Image.open("pbox_datum.png").convert("L")
    pbox = np.array(pbox.resize([15, 31]))
    
    # Get edges of image and detect against
    edges = cv.Canny(img, 100, 200)
    detect = cv.matchTemplate(edges, pbox, cv.TM_CCOEFF_NORMED)
    
    threshy, threshx = [], []

    # Move threshold to find two best values
    t_value = 0.7
    while len(threshy) != 2:
        threshy, threshx = np.where(detect > t_value*np.max(detect))
        if len(threshy) > 2:
            t_value *= 1.01
        elif len(threshy) < 2:
            t_value *= 0.98
        
    loc1 = [threshx[0], threshy[0]]
    loc2 = [threshx[1], threshy[1]]
    
    # Threshold for black lines
    black = np.zeros(img.shape, dtype="uint8")
    black[np.where(img<=10)] = 255
    
    # Generate horizontal edges
    box1_top = loc1[1] - 25
    box2_top = loc2[1] - 25
    box1_bottom = loc1[1] + 35
    box2_bottom = loc2[1] + 35
    
    # Get vertical lines to either side of detected locations
    search1 = np.sum(black[box1_top:box1_bottom], 0)
    columns = np.where(search1 >= max(search1)//2)[0]
    index = bisect(columns, loc1[0])
    box1_left = columns[index-1]
    box1_mid = columns[index]
    box1_right = columns[index+2]
    
    search2 = np.sum(black[box2_top:box2_bottom], 0)
    columns = np.where(search2 >= max(search2)//2)[0]
    index = bisect(columns, loc2[0])
    box2_left = columns[index-1]
    box2_mid = columns[index]
    box2_right = columns[index+2]
    
    box1 = [box1_left, box1_top, box1_right, box1_bottom, box1_mid]
    box2 = [box2_left, box2_top, box2_right, box2_bottom, box2_mid]
    
    return box1, box2


def find_map_box(img):
    
    beige = np.zeros(img.shape, dtype="uint8")
    beige[np.where(img==240)] = 255
    edges = cv.Canny(beige, 100, 200)//255
    
    x_edges = np.sum(edges, 0)
    
    y = edges.shape[0]//2
    map_left = 0
    map_right = 0
       
    # Find map vertical edges
    columns = np.where(x_edges >= y)[0]
    index = bisect(columns, edges.shape[1]//2)
    map_left = columns[index-1]+2
    map_right = columns[index]
        
    # Find map box horizontal edges, cut at map vertical edges
    y_edges = np.sum(edges[:, map_left:map_right], 1)
    
    x = (map_right-map_left)//2
    map_top = 0
    map_bottom = 0
    
    rows = np.where(y_edges >= x)[0]
    map_top = rows[3]+2
    map_bottom = rows[4]
    
    map_box = [map_left, map_top, map_right, map_bottom]
    
    return map_box


def find_tiles(map_img, tileset):
    map_abstract = np.full([14, 18], 255, dtype="uint8")
    for i, tile in enumerate(tileset):
        detect = cv.matchTemplate(map_img, tile, cv.TM_CCOEFF_NORMED)
        good = np.where(detect > 0.9)
        map_abstract[good[0]//20, good[1]//20] = i
    
    return map_abstract


def regenerate_map_image(map_abstract, tileset):
    x, y = map_abstract.shape
    map_img = np.zeros([x*20, y*20, 3], dtype="uint8")
    for x, row in enumerate(map_abstract):
        for y, tile in enumerate(row):
            if tile == 255:
                continue
            map_img[20*x:20*(x+1), 20*y:20*(y+1), :] = tileset[tile]
        
    return map_img

map_img = Image.open("map_test.png")
map_img = np.array(map_img)[:,:,:3]

tileset = [np.array(Image.open("forest.png"))[:,:,:3],
           np.array(Image.open("grass.png"))[:,:,:3],
           np.array(Image.open("bridge.png"))[:,:,:3]]


map_abstract = find_tiles(map_img, tileset)
map_regen = regenerate_map_image(map_abstract, tileset)
        
# scn = Screenshotter()
# grey = scn.take_screenshot()
# img = Image.open("AWBW2.png")
# grey = img.convert("L")
# grey = np.array(grey)
# grey = np.array(grey.crop([500, 200, 1300, 700]))


# map_box = find_map_box(grey)
# pbox1, pbox2 = find_pboxes(grey)

# cv.rectangle(grey, map_box[:2], map_box[2:], 0, 3)
# cv.rectangle(grey, pbox1[:2], pbox1[2:4], 0, 3)
# cv.rectangle(grey, pbox2[:2], pbox2[2:4], 0, 3)


# map_img = grey[map_box[1]:map_box[3], map_box[0]:map_box[2]]

# plt.imshow(map_img, cmap='gray')