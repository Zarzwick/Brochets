#! /usr/bin/env python

"""
Example demonstrating the use of LBP from SciKit and fft from Numpy.

It is advised, for now, to use it with a cropped image since we have no quick
way to access the associated JSON. What I would do (this is to discuss) is to
take the json and an index instead of the image, so we can access the bounding
box and crop here directly.
"""

# Import arrays, image basic functions...
from numpy import *
from numpy.fft.fftpack import *
from numpy.fft.helper import *
from scipy.signal import convolve2d as conv2
import matplotlib.pyplot as plt

# Import LBP from SciKit
from skimage.feature import local_binary_pattern


# Check an image argument is provided.
import sys
if len(sys.argv) != 2:
    #imagePath = '../../local/CAMPAGNE1-150414/IMG_0090.JPG'
    print("Usage: {} IMAGE".format(sys.argv[0]))
    sys.exit(1)
else:
    imagePath = sys.argv[1]


# Read a picture (output a numpy.ndarray).
image = plt.imread(imagePath)

# Extract a color (the green one) if RGB.
if len(shape(image)) > 2 and shape(image)[2] > 1:
    image = image[:, :, 1]

plt.figure('Image')
plt.imshow(image)

# Remove scales (les écailles, quoi).
imageFFT = fft2(image)

plt.figure('FFT')
plt.imshow(log(abs(fftshift(imageFFT))))

# Define a mask for the module of the Fourier transform.
# IIRC There is a discussion on this in the internship report,
# in order to improve this filtering.
mask = zeros(shape(imageFFT))
center = (int(shape(mask)[0]/2), int(shape(mask)[1]/2))
mask[center[0], center[1]] = 1 # Dirac
f = reshape(blackman(1000), (1, -1))
mask = conv2(mask, f, 'same')
mask = conv2(mask, transpose(f), 'same')

plt.figure('Mask')
plt.imshow(mask)

# Apply it.
module = fftshift(mask*abs(fftshift(imageFFT)))
imageWithoutScales = abs(ifft2(module * exp(1j*angle(imageFFT))))

plt.figure('Filtered image')
plt.imshow(abs(imageWithoutScales))

plt.figure('Difference')
plt.imshow(imageWithoutScales - image)

# LBP
imageLBP = local_binary_pattern(imageWithoutScales, 8, 2)

plt.figure('Image LBP')
plt.imshow(imageLBP)

plt.show()

