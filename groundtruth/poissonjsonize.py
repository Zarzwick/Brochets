#! /usr/bin/env python
#  Convert data from imglab's XML to json

import xml.etree.ElementTree as xml
import json
import sys


if len(sys.argv) != 2:
	print('Usage: {} XML_FILE'.format(sys.argv[0]))
        sys.exit(1)
else:
	xmlFile = sys.argv[1]

# Read XML
xmlDataset = xml.parse(xmlFile)
xmlRoot = xmlDataset.getroot()
xmlImages = xmlRoot[2]

# Create a list from it
fishes = {}

for xmlImage in xmlImages:
	fileName = xmlImage.attrib['file']
	fish = {'id': ''}

	fishBoxes = [node for node in xmlImage if node.tag == 'box']

	for box in fishBoxes:
		label = box[0].text
		if label == 'fish':
			label = 'outer'
		else:
			label = 'inner'
		
		coords = box.attrib
		fish[label] = [coords['top'], coords['left'], coords['width'], coords['height']]

	fishes[fileName] = fish

# Dump to JSON
print(json.dumps(fishes, indent=4, separators=(',', ': ')))

