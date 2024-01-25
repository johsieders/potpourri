# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 12:23:14 2023

@author: c8451226
"""

# importing "cmath" for complex number operations
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from colorschemes import colorscheme_maxvalues
from create_grid import create_grid
from julia import julia


# Define the update function for the slider
def update(val):
    c_real = slider_real.val
    c_imag = slider_imag.val
    constant = complex(c_real, c_imag)

    results = []
    results.append(julia(zets, constant, num_iterations)[0])
    results = results[0]

    # calculate normalized results for colorscheme
    results_normalized = colorscheme_maxvalues(results)

    # calculate colorscheme according to maximum counts
    counter = []
    counter.append(julia(zets, constant, num_iterations)[1])
    counter = counter[0]

    ax.tripcolor(zets_real, zets_imag, counter, cmap='plasma', shading='flat')
    fig.canvas.draw_idle()


# iterate over all constants
num_iterations = 20
constant = complex(0, 0)
resolution = 50
limx_low = -2
limx_high = 2
limy_low = -2
limy_high = 2

# calculate grid
zets = create_grid(resolution, limx_low, limx_high, limy_low, limy_high)
zets_real = [z.real for z in zets]
zets_imag = [z.imag for z in zets]

# calculate julia set
julia_results = []
julia_results.append(julia(zets, constant, num_iterations)[0])
julia_results = julia_results[0]

# calculate colorscheme according to maximum counts
counter = []
counter.append(julia(zets, constant, num_iterations)[1])
counter = counter[0]

# calculate colorscheme according to maximum values
# results_normalized = colorscheme_maxvalues(julia_results)

# PLOT
fig, ax = plt.subplots()
ax.tripcolor(zets_real, zets_imag, counter, cmap='plasma', shading='gouraud')
ax.set_xlim([limx_low, limx_high])
ax.set_ylim([limy_low, limy_high])

# SLIDER
# Add a slider for changing a variable (in this case, frequency)
ax_slider_real = plt.axes([0.2, 0.01, 0.65, 0.01], facecolor='lightgoldenrodyellow')
slider_real = Slider(ax_slider_real, 'c_real', -2.0, 2.0, valinit=0.0)

ax_slider_imag = plt.axes([0.2, 0.04, 0.65, 0.01], facecolor='lightgoldenrodyellow')
slider_imag = Slider(ax_slider_imag, 'c_imag', -2.0, 2.0, valinit=0.0)

# Attach the update function to the slider
slider_real.on_changed(update)
slider_imag.on_changed(update)
