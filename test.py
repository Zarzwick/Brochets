# 3 lines.
import json
data = json.load(open('groundtruth/example.json'))
print("Fish {} as a bounding box.".format(data['id']))

