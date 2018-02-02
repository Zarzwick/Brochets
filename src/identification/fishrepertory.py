#!  /usr/bin/env python
import json
from numpy import array
from typing import Tuple
from fish import Fish, FishName
import csv


class FishRepertory(object):
    '''
    Store the log of fishes.
    For each fish, we have nCampaigns tuple with the fish ID (name) in each campaign.
    '''

    def __init__(self, fileName='../../groundtruth/suivi.csv'):
        '''Load the csv of the fishes log.'''

        self.fishesRef = []

        with open(fileName) as file:
            file.readline()
            reader = csv.reader(file)

            for row in reader:
                countCampaign = len(row) // 2
                fish = []

                # Column of ID : 1, 3, 5, 7, ...
                for c in range(countCampaign):
                    id = row[1 + c * 2]

                    if id != '':
                        fish.append((c + 1, str(id)))
                    else:
                        fish.append(None)

                self.fishesRef.append(fish)



    def are_the_same(self, fishA: FishName, fishB: FishName):
        '''Check if two fishes are the same (check theirs IDs through campaigns)'''

        if fishA[0] == fishB[0] and fishA[1] == fishB[1]:
            return True

        else:
            # Check each row.
            for ref in self.fishesRef:

                refA = ref[fishA[0] - 1]
                refB = ref[fishB[0] - 1]

                # Check if is there a reference for each fish.
                if refA is not None and refB is not None:
                    # If fishes are on the same row, they are the same.
                    if refA[1] == fishA[1] and refB[1] == fishB[1]:
                        return True

        return False        



    def get_fish_row(self, fish: FishName):
        '''Retrieve row number of the fish in the log file.'''

        rowID : int = 0
        # Check each row.
        for ref in self.fishesRef:
            refA = ref[fish[0] - 1]
            if refA is not None:
                # If fishes are on the same row, they are the same.
                if refA[1] == fish[1]:
                    print(rowID)
                    return rowID
            
            rowID = rowID + 1

        # Couldn't find the corresponding row.
        return -1
