#!  /usr/bin/env python
import json
from matplotlib.pyplot import imread, imshow
from numpy import array
from typing import Tuple
from fish import Fish

class FishLoader(object):
    '''Permanent fish loader
    Load once all the jsons then fish pictures can be accessed with [] operator'''

    def __init__(self, countCampaign : int=4):
        '''Load all JSONS of the campaigns.'''

        self.dataCampaigns = []
        
        for i in range(countCampaign):
        
            pathToJson = '../../groundtruth/campagne-' + str(i + 1) + '.json'   
            jsonContent = open(pathToJson).read()
            
            self.dataCampaigns.append(json.loads(jsonContent))



    def __getitem__(self, key: Fish):
        '''Retrieve an fish image from a given campaign ID and fish number, [campaignID, fishNumber]
        Campaign ID are from 1 to countCampaign (constructor parameter)
        Fish number are from 0 to count of fish in the json'''

        try:
            dataCampaign = self.dataCampaigns[key[0] - 1]
            fishKeys = list(dataCampaign)
            idFish = fishKeys[key[1]]

            dataFish = dataCampaign[idFish]

            pathToPicture = '../../local/' + idFish
            bounds = dataFish['outer']
            
            topLeft = array([int(bounds[1]), int(bounds[0])])
            bottomRight = topLeft + array([int(bounds[3]), int(bounds[2])])

            fish = imread(pathToPicture)
            fish = fish[topLeft[0]:bottomRight[0], topLeft[1]:bottomRight[1], 1]

        except KeyError:
           print('There is not such fish')
          
        return fish
