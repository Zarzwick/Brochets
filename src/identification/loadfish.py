
import json
from matplotlib.pyplot import imread, imshow
from numpy import array



def load_fish(idCampaign: int, idFish: int):

	pathToJson = '../../groundtruth/campagne-' + str(idCampaign) + '.json'

	jsonContent = open(pathToJson).read()

	data = json.loads(jsonContent)

	fishKeys = list(data)

	try:
		dataFish = data[fishKeys[idFish]]

		pathToPicture = '../../local/' + fishKeys[idFish]

		bounds = dataFish['outer']
		print(bounds)

		topLeft = array([int(bounds[0]), int(bounds[1])])
		bottomRight = topLeft + array([int(bounds[3]), int(bounds[2])])

		fish = imread(pathToPicture)
		fish = fish[topLeft[0]:bottomRight[0], topLeft[1]:bottomRight[1], 1]

	except KeyError:
		print('There is not such fish')

	
	imshow(fish)

	return fish	