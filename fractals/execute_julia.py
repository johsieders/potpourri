# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 12:23:14 2023

@author: c8451226
"""

# importing "cmath" for complex number operations
import matplotlib.pyplot as plt

from colorschemes import colorscheme_maxvalues
from create_grid import create_grid
from julia import julia

# Initial conditions
num_iterations = 200
constant = complex(0.0, -1.0)
resolution = 1000
limx_low = -2
limx_high = 2
limy_low = -2
limy_high = 2

# calculate grid
zets = create_grid(resolution, limx_low, limx_high, limy_low, limy_high)
zets_real = [z.real for z in zets]
zets_imag = [z.imag for z in zets]

# calculate Juliaset
julia_results = []
julia_results.append(julia(zets, constant, num_iterations)[0])
julia_results = julia_results[0]

# calculate colorscheme according to maximum counts
counter = []
counter.append(julia(zets, constant, num_iterations)[1])
counter = counter[0]

# calculate colorscheme according to maximum values
results_normalized = colorscheme_maxvalues(julia_results)

# PLOT
# plt.tripcolor(zets_real, zets_imag, results_normalized, cmap = 'plasma', shading='gouraud')
plt.tripcolor(zets_real, zets_imag, counter, cmap='gnuplot_r', shading='gouraud')

# plt.scatter(zets_real, zets_imag, c=counter, s=1)

plt.xlim([limx_low, limx_high])
plt.ylim([limy_low, limy_high])
plt.show()
