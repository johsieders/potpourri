# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 14:48:42 2023

@author: c8451226
"""


def mandelbrot(constant, num_iterations):
    z = 0.0
    count = 0
    counter = []
    result = []
    for i in range(num_iterations):
        z = z ** 2 + constant
        if abs(z.real) > 1e10:
            break
        if abs(z.imag) > 1e10:
            break
        result.append(z)
        count += 1
        counter.append(count)
    return result, counter
