#!  /usr/bin/env python
from fishloader import FishLoader
from fish import Fish
from lbphistogram import lbp_histrogram
from typing import Tuple
from chidistance import weighted_chi_square_distance

def best_match(fish: Fish, candidates, sort: bool, chiWeights = [1]*36 ):
    '''
    Find the closest fishes in candidates to the fish
    chiWeights used for distances calculations.
    '''

    fishLoader = FishLoader()

    fishImage = fishLoader[fish]
    fishHist = lbp_histrogram(fishImage)

    distances = []

    for candidate in candidates:

        candidateImage = fishLoader[candidate]
        candidateHist = lbp_histrogram(candidateImage)

        distance = weighted_chi_square_distance(fishHist, candidateHist, chiWeights)

        distances.append((candidate, distance))

    if( sort ):
        # Sort according to the distance.
        distances = sorted(distances, key=lambda tuple: tuple[1])

    return distances

