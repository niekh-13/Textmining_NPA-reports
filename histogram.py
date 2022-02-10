##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    histogram maker                                         #
#                                                            #
##############################################################

# Import the relevant packages
from Textmining_ETZ.util.VisualizeData import VisualizeDataset
import pandas as pd
import os
from pathlib import Path

DataViz = VisualizeDataset(__file__)

# input files and directories
DATA_PATH = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TRAIN')
# DATA_text = Path('/home/niek/Documents/ETZ/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TRAIN')
# DATASETS = []

for filename in os.listdir(DATA_PATH):
    if 'X_train' in filename:
        file = os.path.join(DATA_PATH, filename)
        file = os.path.abspath(file)
        DATA = pd.read_csv(file)
        name = filename.split('.csv')[0]
        bin = 20
        DataViz.histogram(DATA, bin)
        # DATASETS.append(DATA)

#
# RESULT_DATA = reduce(lambda  left,right: pd.merge(left,right,on=['ID'],
#                                             how='outer'), DATASETS)
#
# RESULT_DATA = RESULT_DATA[['ID', 'T0_obs_truth', 'T0_ptnt_obs', 'T3_obs_truth', 'T3_ptnt_obs', 'T12_obs_truth','T12_ptnt_obs']]
# RESULT_DATA = RESULT_DATA.sort_values(by=['ID'], ascending=[True])
# DataViz.missing_values(RESULT_DATA)
