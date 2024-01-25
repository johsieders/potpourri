# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 12:08:14 2023

@author: c8451226
"""


def julia(zets, constant, num_iterations):
    c = constant
    result = []
    counter = []
    for z in zets:
        count = 0
        for i in range(num_iterations):
            z = z ** 2 + c
            if abs(z.real) > 1e100:
                break
            if abs(z.imag) > 1e100:
                break
            count += 1
        result.append(z)
        counter.append(count)
    return result, counter
