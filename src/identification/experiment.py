#! /usr/bin/env python

'''
An experiment trying to implement the main paper,
without taking in account the good LBP parameters.

This for now is all about creating the histogram.
'''

from numpy import *
from matplotlib.pyplot import imread, plot
from tilediterator import TiledIterator
from skimage.feature import local_binary_pattern as lbp
from typing import Mapping


# Check an image argument is provided.
import sys
if len(sys.argv) != 2:
    imagePath = '../../local/CAMPAGNE1-150414/IMG_0090.JPG'
    image = imread(imagePath)
    image = image[760:1300, 710:3360, 1]
    #print("Usage: {} IMAGE".format(sys.argv[0]))
    #sys.exit(1)
else:
    imagePath = sys.argv[1]
    image = imread(imagePath)

#imagev = reshape(image, (-1, 1))

# Here I define the LBP parameters as a tuple.
LBPParams = Tuple[int, int] # type: A triplet (P, R)
lbpParams = (8, 2)

# In the paper, 2-uniforms LBP are used. As we will later need to know
# the number of labels a LBP can produce (n), it is defined here:
def n_for_2_uniform_lbp(lbpParams: LBPParams) -> int:
    return 2 + P*(P-1)

# Unformal proof of this (on P = 4)
# I consider the length l of the 111...111 inside the pattern.
# Two edge cases: l = 0: 0000 and l = P: 1111.
# For each l in ]0, P[ (3 possible = P-1):
# 1000 0100 0010 0001
# 1100 0110 0011 1001
# 1110 0111 1011 1101
# <------- P ------->
#
# We have to generate a mapping from those values to {0, 1, ..., n-1} in order
# to put them in an histogram. n will be any pattern not matching u2.
def lut(P: int) -> Mapping[int, int]
    return None # It's a WIP
    m = {}
    acc = 0
    # For 000..000
    m[0] = acc
    # For each intermediary length:
    for l in range(1, P):
        acc += 1
        # Compute each circular shift:
        for shift in range(0, P):
            # TODO
            m[] = acc
    # And finally, for 111..111
    m[(2**P)-1] = acc
    return m

# The goal is to subdivide the picture in different ways (3 here) and to
# concatenate their histograms.
subdivs = [(3, 12)]#, (4, 16)]

# Here is the computation of one histogram (defined in Face Recognition with
# Local Binary Patterns).
# We shall first find n (the number of possible values of LBP) and m (the 
# number of regions). Note that n += 1 because we want a value that represent
# non-uniformity.
subdiv = subdivs[0]
n = n_for_2_uniform_lbp(lbpParams) + 1
m = subdiv[0] * subdiv[1]

# Then, we have an histogram that consists of the concatenation of m
# histograms, each one of size n. It means, for one region we keep
# the number of pixels that represent a label of LBP.
# Jehan, note that I preallocated the table ! In python !
lbpHist = zeros((m, n))
lbpImage = lbp(image, lbpParams[0], lbpParams[1])
labelMap = lut(lbpParams[0])

for tileBounds in TiledIterator(lbpImage, subdiv):
    tile = image[tileBounds]
    size = tileBounds.subshape
    for row in range(size[0]):
        for col in range(size[1]):
            label = tile[row, col]
            lbpHist[labelMap[label]] += 1

