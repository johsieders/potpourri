# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 14:34:21 2023

@author: c8451226
"""

import numpy as np


def create_grid(resolution, limx_low, limx_high, limy_low, limy_high):
    grid_real = np.linspace(limx_low, limx_high, resolution)
    grid_imag = np.linspace(limy_low, limy_high, resolution)
    grid = []
    for real in grid_real:
        for imag in grid_imag:
            grid.append(complex(real, imag))
    return grid
