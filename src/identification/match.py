#!  /usr/bin/env python
from fishloader import FishLoader
from fish import Fish
from lbphistogram import lbp_histrogram
from typing import Tuple
from chidistance import weighted_chi_square_distance

def best_match(fish: Fish, candidates, sort: bool, chiWeights=[1] * 36):
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

    if(sort):
        # Sort according to the distance.
        distances = sorted(distances, key=lambda tuple: tuple[1])

    return distances




def cross_match_from_hist(fishesData, chiWeights=[1] * 36):
    '''Compare a serie of fishesData from generateresults.py between them, and fill the distances[] slot with the results.'''

    fishesDataWithDistances = []

    # Process all fishes between them.
    for fishDataA in fishesData:
        distances = []
         
        # Compare fish A with all other fishes.  Slot 2 is the fish lbp
        # histogram.
        for fishDataB in fishesData:
            distance = weighted_chi_square_distance(fishDataA[2], fishDataB[2], chiWeights)
            distances.append(distance)

        # Store the results
        fishesDataWithDistances.append((fishDataA[0], fishDataA[1], fishDataA[2], distances, fishDataA[4]))

    return fishesDataWithDistances

