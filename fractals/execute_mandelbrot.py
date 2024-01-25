# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 11:52:02 2023

@author: c8451226

"""

# importing "cmath" for complex number operations
import matplotlib.pyplot as plt

from colorschemes import colorscheme_maxvalues
from create_grid import create_grid
from mandelbrot import mandelbrot

# iterate over all constants
num_iterations = 200
resolution = 500
limx_low = -3
limx_high = 2
limy_low = -1.5
limy_high = 1.5

grid = create_grid(resolution, limx_low, limx_high, limy_low, limy_high)
mandelbrot_results = []
counter = []
for constant in grid:
    mandelbrot_results.append(mandelbrot(constant, num_iterations)[0][-1])
    counter.append(mandelbrot(constant, num_iterations)[1][-1])

# calculate colorscheme according to maximum values
results_normalized = colorscheme_maxvalues(mandelbrot_results)

constants_real = [constant.real for constant in grid]
constants_imag = [constant.imag for constant in grid]

plt.tripcolor(constants_real, constants_imag, counter, cmap='gnuplot_r', shading='gouraud')
plt.xlim([limx_low, limx_high])
plt.ylim([limy_low, limy_high])
plt.show()
