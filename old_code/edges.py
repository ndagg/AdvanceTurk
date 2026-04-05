# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 19:14:14 2025

@author: ndagg
"""

from PIL import Image

import matplotlib.pyplot as plt

import cv2 as cv
import numpy as np



img = Image.open("AWBW.png")
grey = img.convert("L")
# grey = np.array(grey.crop([500, 200, 1300, 700]))
grey = np.array(grey)


pbox = Image.open("pbox_datum.png").convert("L")
# pbox = np.array(pbox)
pbox = np.array(pbox.resize([17, 40]))



edges = cv.Canny(grey, 100, 200)

plt.imshow(edges)


