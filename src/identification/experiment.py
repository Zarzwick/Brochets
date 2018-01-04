#! /usr/bin/env python

'''
An experiment trying to implement the main paper,
without taking in account the good LBP parameters.

This for now is all about creating the histogram.
'''

from numpy import *


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


# This is one of the strangest things of numpy, but the following line
# is actually the simplest way to get a standard image histogram.
histBins = list(range(257))


# ...

