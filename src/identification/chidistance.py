#! /usr/bin/env python

# This module could be interesting, however it is not weighted.
#from scipy.stats import chisquare

from numpy import array, shape, divide, zeros_like

def weighted_chi_square_distance(h1, h2, regionsWeights) -> float:
    # The goal here is to compute the X² distance between h1 and h2.
    (regions, bins) = shape(h1)
    distance = 0

    for region in range(regions):
        w = regionsWeights[region]
        num = (h2[region] - h1[region])**2
        den = (h2[region] + h1[region])
        distance += w * sum(divide(num, den, out=zeros_like(num), where=den!=0))
    
    return distance

