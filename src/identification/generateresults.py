#!  /usr/bin/env python
from fish import Fish, FishName
from fishrepertory import FishRepertory
from fishloader import FishLoader
from match import best_match
import csv
from numpy import array
from typing import Tuple
from random import randint


def generate_random_fish_results(countCandidates: int=5):
    '''Process the comparisons between one random fish with himself and "countcandidates" others random fishes'''

    fishRepertory = FishRepertory()
    fishLoader = FishLoader()

    # Find a valid random fish to compare.
    subject = None
    while subject is None:
        subjectID = randint(0, len(fishRepertory.fishesRef) - 1)
        subjectCampaign = randint(0, len(fishRepertory.fishesRef[subjectID]) - 1)

        subject = fishRepertory.fishesRef[subjectID][subjectCampaign]

        if subject is not None and len(fishLoader.get_fish_by_name(subject)) == 0:
            subject = None

    # Generate random valid fishes to compare with.
    candidates = []
    while len(candidates) < countCandidates:
        candidateID = randint(0, len(fishRepertory.fishesRef) - 1)
        candidateCampaign = randint(0, len(fishRepertory.fishesRef[candidateID]) - 1)

        candidate = fishRepertory.fishesRef[candidateID][candidateCampaign]

        if(candidate is not None):
            candidates.append(candidate)

    fileName = "../../results/fish" + str(subject[1]) + ".csv"

    generate_fish_results(subject, candidates, fishRepertory, fishLoader, fileName)



def generate_fish_results(fishName: FishName, candidatesNames, fishRepertory: FishRepertory, fishLoader: FishLoader, fileName):
    '''Compare the fishes corresponding the given name with all other fishes. Then save the result in a file.'''

    candidates = []

    subjects = fishLoader.get_fish_by_name(fishName)

    for subject in subjects:
        candidates.append(subject)

    # Test purpose.
    # candidates.append(fishLoader.get_fish_by_name(fishRepertory.fishesRef[0][1])[0])

    for candidateName in candidatesNames:
        for candidate in fishLoader.get_fish_by_name(candidateName):
            candidates.append(candidate)

    distances = []
    
    print("Subject : " + str(subjects))
    print("Candidates : " + str(candidates))

    step : int = 0
    print("Progression : " + str(step) + "/" + str(len(subjects)))

    # For each fishes corresponding to the fish name, process matching.
    for fish in subjects:
        distances.append(best_match(fish, candidates, False))
        step = step + 1
        print("Progression : " + str(step) + "/" + str(len(subjects)))

    save_results(subjects, candidates, fishRepertory, fishLoader, distances, fileName)



def save_results(subjects, candidates, fishRepertory: FishRepertory, fishLoader: FishLoader, results, fileName):

    print('Writting result to file')
    with open(fileName, 'w') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',')


        rowCampaign = ["Subject/Candidate Campaign", "", "", ""]
        rowGround = ["", "Number in Json", "", ""]
        rowLog = ["", "", "Row in Log", ""]
        row = ["", "", "", "Name"]

        # Write candidate name.
        for result in results[0]:
            print("Result : " + str(result))
            candidateName = fishLoader.get_name(result[0])
            print("Result Name : " + str(candidateName))
            rowCampaign.append(candidateName[0])
            rowGround.append(result[0][1])
            rowLog.append(fishRepertory.get_fish_row(candidateName))
            row.append(candidateName[1])

        csvWriter.writerow(rowCampaign)
        csvWriter.writerow(rowGround)
        csvWriter.writerow(rowLog)
        csvWriter.writerow(row)

        # Write the result for each subject.
        subjectID : int = 0
        for subjectResults in results:
            
            subjectName = fishLoader.get_name(subjects[subjectID])
            row = [subjectName[0], subjects[subjectID][1], fishRepertory.get_fish_row(subjectName), subjectName[1]]

            for result in subjectResults:
                row.append(result[1])

            csvWriter.writerow(row)
            subjectID = subjectID + 1




#######################################################################################################################
# All results
#######################################################################################################################
from typing import Tuple
from fish import *
from lbphistogram import *
from fishloader import FishLoader
from fishrepertory import FishRepertory
import json
import csv
from match import cross_match_from_hist

# ResultType = Tuple(FishName, Fish, array, distance[], photoName)
fishLoader = FishLoader()
fishRepertory = FishRepertory()

fishesData = []


# Process all lbp histograms once for all.
progressFish = 0
for fish in fishRepertory.fishesRef:
    for fishName in fish:
        if fishName is not None:
            fishPhotos = fishLoader.get_fish_by_name(fishName)

            progressPhoto = 0
            for fishPhoto in fishPhotos:
                photoInBox = fishLoader[fishPhoto]
                photoFileName = fishLoader.get_fish_photo_name(fishPhoto)
                fishesData.append((fishName, fishPhoto, lbp_histrogram(photoInBox), [], photoFileName))

                progressPhoto = progressPhoto + 1
                print("Progress Fish " + str(progressFish) + " : " + str(fishName) + " " + str(progressPhoto) + "/" + str(len(fishPhotos)))

    progressFish = progressFish + 1



# Save histograms without distances.
save_fishesdata(fishesData, "../../results/LBP_Histograms/lbp_histograms.json")

# Load histograms without distances.
fishesData = load_fishesdata("../../results/LBP_Histograms/lbp_histograms.json")



# Process distances between histograms
fishesDataWithDistances = cross_match_from_hist(fishesData)



# Save histograms (distances are calculated now).
save_fishesdata(fishesDataWithDistances, "../../results/LBP_Histograms/lbp_histograms_with_distances.json")

# Load histograms with distances.
fishesDataWithDistances = load_fishesdata("../../results/LBP_Histograms/lbp_histograms_with_distances.json")



save_results_to_csv(fishesDataWithDistances, "../../results/distances_results.csv", fishRepertory)




# Save and load functionnalities for histograms
def save_fishesdata(fishesData, fileName):
    with open(fileName, 'w') as file:
        fishesToWrite = []
        # Convert numpy array to list for serialization.
        for fishData in fishesData:
            fishesToWrite.append((fishData[0], fishData[1], fishData[2].tolist(), fishData[3], fishData[4]))

        json.dump(fishesToWrite, file)



def load_fishesdata(fileName):
    with open(fileName) as file:
        fishesDataLoadedJson = json.load(file)
        fishesData = []
        for fishData in fishesDataLoadedJson:
            fishName = tuple(fishData[0])
            fishPhoto = tuple(fishData[1])
            fishesData.append((fishName, fishPhoto, array(fishData[2]), fishData[3], fishData[4]))

    return fishesData

def save_results_to_csv(fishesData, fileName, fishRepertory : FishRepertory):

    with open(fileName, 'w') as csvfile:
        csvWriter = csv.writer(csvfile)

        rowCampaign = ["Campaign", "", "", ""]
        rowPhotoName = ["", "Photo name", "", ""]
        rowLog = ["", "", "Row in log", ""]
        rowName = ["", "", "", "ID in log"]

        # Abscissa axis infos.
        for fishData in fishesData:
            rowCampaign.append(fishData[0][0])
            rowPhotoName.append(fishData[4])
            rowLog.append(fishRepertory.get_fish_row(fishData[0]))
            rowName.append(fishData[0][1])

        csvWriter.writerow(rowCampaign)
        csvWriter.writerow(rowPhotoName)
        csvWriter.writerow(rowLog)
        csvWriter.writerow(rowName)

         # Ordinate axis infos and distances.
        for fishData in fishesData:
            row = [fishData[0][0]] # Campaign
            row.append(fishData[4]) # Photo Name
            row.append(fishRepertory.get_fish_row(fishData[0])) # Row in log file
            row.append(fishData[0][1]) # Fish Name

            for distance in fishData[3]:
                row.append(distance) # Distances

            csvWriter.writerow(row)
