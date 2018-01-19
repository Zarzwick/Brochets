#!  /usr/bin/env python

import json
from numpy import array
from typing import Tuple
from fish import Fish, FishName
import csv


class FishRepertory(object):
	'''Store the log of fishes.
	For each fish, we have nCampaigns tuple with the fish ID (name) in each campaign.'''

	def __init__(self, fileName = '../../groundtruth/suivi.csv' ):
		'''Load the csv of the fishes log.'''

		self.fishesRef = []

		with open( fileName ) as file:
			file.readline();
			reader = csv.reader( file )

			for row in reader:
				countCampaign = len( row ) // 2
				fish = []

				# Column of ID : 1, 3, 5, 7, ...
				for c in range(countCampaign):
					id = row[1 + c * 2]

					if id != '':
						fish.append( (c+1, str(id) ) )
					else:
						fish.append( None )

				self.fishesRef.append( fish )
