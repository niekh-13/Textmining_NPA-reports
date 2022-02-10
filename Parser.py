##############################################################
#                                                            #
#    Niek Huijsmans  (2021)                                  #
#    Textmining medical notes for cognition                  #
#    Parser                                                  #
#                                                            #
##############################################################

import os
import pandas as pd
from Parser.ParseDataset import ParseDataset
from util.VisualizeData import VisualizeDataset
from pathlib import Path

# input files and directories
DATASET = Path('./cleaned_medical_notes/')
RESULT = Path('./intermediate_datafiles')
OUTPUT = 'Parsed_Notes.csv'

DataViz = VisualizeDataset(__file__)

# We can call Path.mkdir(exist_ok=True) to make any required directories if they don't already exist.
[path.mkdir(exist_ok=True, parents=True) for path in [RESULT]]

datasets = pd.DataFrame()

for i, filename in enumerate(os.listdir(DATASET)):
    if filename.endswith(".txt"):

        print('This is file: ' + filename + " (" + str(i) + '/' + str(len(os.listdir(DATASET))) + ")")

        filename = os.path.join(DATASET, filename)
        filename = os.path.abspath(filename)
        file = open(filename, mode='r', encoding='UTF-8')
        file = file.read()
        dataset = ParseDataset(filename, file, i)
        #create initial dataset with ID code and if it was a re-resection surgery
        dataset.create_dataset()
        #We now add pre test and question data of the medical notes to the dataset
        dataset.pre_parser()
        #We now add the T0 test and obs data of the medical notes to the dataset
        dataset.T0_parser()
        # We now add the T3 test and obs data of the medical notes to the dataset
        dataset.T3_parser()
        # We now add the T12 test and obs data of the medical notes to the dataset
        dataset.T12_parser()
        # Get the resulting pandas dataframe
        dataset = dataset.data_table
        # Concatenate all rows to final dataset
        datasets = pd.concat([datasets, dataset])

datasets.to_csv(RESULT / OUTPUT, index=False)

DataViz.missing_values(datasets)
