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
        subjectCampaign = randint(0, len(fishRepertory.fishesRef) - 1)
        subjectID = randint(0, len(fishRepertory.fishesRef[subjectCampaign]) - 1)

        subject = fishRepertory.fishesRef[subjectCampaign][subjectID]

        if subject is not None and len( fishLoader.get_fish_by_name( subject ) ) == 0:
            subject = None

    # Generate random valid fishes to compare with.
    candidates = []
    while len(candidates) < countCandidates:
        candidateCampaign = randint(0, len(fishRepertory.fishesRef) - 1)
        candidateID = randint(0, len(fishRepertory.fishesRef[candidateCampaign]) - 1)

        candidate = fishRepertory.fishesRef[candidateCampaign][candidateID]

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
            subjectID = subjectID + 1;

