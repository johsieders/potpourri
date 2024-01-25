# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 14:30:34 2023

@author: c8451226
"""
import math

import numpy as np

from julia import julia
from mandelbrot import mandelbrot


def colorscheme_counter_mandelbrot(grid, constant, num_iterations):
    counter = []
    counter.append(mandelbrot(constant, num_iterations)[1])
    counter = counter[0]
    return counter


def colorscheme_counter_julia(grid, constant, num_iterations):
    counter = []
    counter.append(julia(grid, constant, num_iterations)[1])
    counter = counter[0]
    return counter


def colorscheme_maxvalues(julia_results):  # projects the results on a range from 0 to 1 based on a log10 function
    julia_results_abs = [abs(number) for number in julia_results]
    julia_results_real_max = max([abs(value) for value in julia_results_abs])
    exponent = int(math.log10(julia_results_real_max))
    results_normalized = np.log10([abs(value) for value in julia_results_abs]) / exponent
    results_normalized = [max(value, 0) for value in results_normalized]  # remove values smaller than 0
    return results_normalized
