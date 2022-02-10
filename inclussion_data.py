##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    Zsc y exclussion                                        #
#                                                            #
##############################################################

# Import the relevant packages
from Textmining_ETZ.util.outlier import OutlierDetection
import numpy as np
import pandas as pd
import os
from pathlib import Path
from sklearn.model_selection import train_test_split
import pyreadstat


# input files and directorie
file_y = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/y_data/TEXT_T0_new-Zsc.sav')
file_x = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/intermediate_datafiles/T0_obs_raw.csv')
RESULT_1 = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TRAIN')
RESULT_2 = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TEST')

# load y data (clinical and nps variables)
file_y = os.path.abspath(file_y)
DATA_y, meta = pyreadstat.read_sav(file_y, apply_value_formats=False)

# load x data (text)
file_x = os.path.abspath(file_x)
DATA_x = pd.read_csv(file_x)

# Drop nan
DATA_x = DATA_x.dropna()
ID_x = DATA_x['ID'].to_list()

# only IDs that are in DATA_x
DATA_y = DATA_y[DATA_y['ID_code'].isin(ID_x)].copy() # 189 patients have no NPS

# filter on PA_diagnose
PA_diagnosis = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,15]

DATA_y = DATA_y[DATA_y['PA_diagnosis'].isin(PA_diagnosis)].copy() # 158 patients do not have PBT

# Remove invald patients (30 patients)
DATA_y = DATA_y.drop(index=[22,28,32,33,35,38,41,107,154,494,507,510,515,536,555,608,635,669,672,730,769,780,807,897,
                            915,917,935,975,1128,1219])
DATA_y.loc[[752,965], 'Zsc_vismem_T0'] = np.nan
DATA_y.loc[[707,570,527,226,187,75,57],'Zsc_verbalmem_T0'] = np.nan
DATA_y.loc[[1123,1020,1018,1007,971,912,878,818,642,518,230,176,137,116,58,108,30],['Zsc_Stroop_simple_T0',
                                                                                    'Zsc_Stroop_interferentie_T0',
                                                                                    'Zsc_Stroop_IIIrt_T0',
                                                                                    'Zsc_complexatt_T0',
                                                                                    'Zsc_cognflex_T0',]] = np.nan
DATA_y.loc[[19,54,57,131,176,214,238,642,818,878,1129,1172],['Zsc_cognflex_T0', 'Zsc_complexatt_T0',
                                                             'Zsc_EF_T0']] = np.nan
DATA_y.loc[[54,95,228,735,1172],['Zsc_psychomsp_T0', 'Zsc_procspeed_T0']] = np.nan
DATA_y.loc[[19,106,161,165,181,1125],['Zsc_motorspeed_T0', 'Zsc_psychomsp_T0']] = np.nan
DATA_y.loc[861,['Zsc_CPT_reactietijd_T0','Zsc_complexatt_T0']] = np.nan

columns = ['Zsc_psychomsp_T0', 'Zsc_reactime_T0', 'Zsc_complexatt_T0', 'Zsc_cognflex_T0','Zsc_procspeed_T0',
           'Zsc_verbalmem_T0', 'Zsc_vismem_T0', 'Zsc_motorspeed_T0','Zsc_EF_T0']

#check for outliers and remove them
for column in columns:
    print(column)
    outlier_removal = OutlierDetection()
    DATA_y_1 = outlier_removal.chauvenet(data_table=DATA_y, col=column)

# drop de patients are not able to normalize the domain scores
DATA_y = DATA_y.dropna(subset=columns, how='all') #  15 patients do not have any domain scores

# Remove the patients also in x data
ID_y = DATA_y['ID_code'].to_list()
DATA_x = DATA_x[DATA_x['ID'].isin(ID_y)].copy()

#sort on id_code
DATA_y = DATA_y.sort_values(['ID_code']).copy()
DATA_x = DATA_x.sort_values(['ID']).copy()

#reset indices for both dataframes
DATA_y = DATA_y.reset_index(drop=True).copy()
DATA_x = DATA_x.reset_index(drop=True).copy()


# split the y and X data in to train an test sets
X_train, X_test, y_train, y_test = train_test_split(DATA_x, DATA_y, test_size=0.1, random_state=2022)

#reset indices for both dataframes
X_train = X_train.reset_index(drop=True).copy()
X_test = X_test.reset_index(drop=True).copy()
y_train = y_train.reset_index(drop=True).copy()
y_test = y_test.reset_index(drop=True).copy()

X_train.to_csv(RESULT_1 / 'X_train.csv', index=False)
y_train.to_csv(RESULT_1 / 'y_train.csv', index=False)
pyreadstat.write_sav(df=y_train, dst_path=RESULT_1 / 'y_train.sav',
                     variable_value_labels=meta.variable_value_labels)

X_test.to_csv(RESULT_2 / 'X_test.csv', index=False)
y_test.to_csv(RESULT_2 / 'y_test.csv', index=False)
pyreadstat.write_sav(df=y_test, dst_path=RESULT_2 / 'y_test.sav',
                     variable_value_labels=meta.variable_value_labels)

