#!/usr/bin/env python3
##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    Final LARS model                                        #
#                                                            #
##############################################################

# Import the relevant packages
from util.VisualizeData import VisualizeDataset
from util.Save import Save
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
import pyreadstat
from pathlib import Path
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from datetime import datetime

begin_time = datetime.now()

DataViz = VisualizeDataset(__file__)
Save_json = Save(__file__)

# input files and directories
file_x = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TRAIN/dutch_bert_embeddings.csv')
file_y = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TRAIN/y_train.sav')
file_x_test = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TEST/dutch_bert_embeddings.csv')
file_y_test = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TEST/y_test.sav')

### import train data ###
#import y dataframe with labels
y_data, meta = pyreadstat.read_sav(file_y, apply_value_formats=False)
x_data = pd.read_csv(file_x)

### import test data ###
X_test_data = pd.read_csv(file_x_test)
y_test_data, meta = pyreadstat.read_sav(file_y_test, apply_value_formats=False)
y_test_data['WHO_grade'] = y_test_data['WHO_grade'].fillna(1)


#take informative features
X_socio = y_data.loc[:, ['ID_code','sex', 'education_high', 'education_low', 'WHO_grade', 'PA_diagnosis', 'age_T0']]
X_socio.rename(columns={'ID_code':'ID'}, inplace=True)
X_socio.loc[32,'WHO_grade'] = 1
X_socio.loc[175,'WHO_grade'] = 3

#make ID str
X_socio['ID'] = X_socio['ID'].astype(str)
x_data['ID'] = x_data['ID'].astype(str)

#merge socio features
X_ds = x_data.merge(X_socio, on='ID', how='inner')

#take informative features
X_socio_test = y_test_data.loc[:, ['ID_code','sex', 'education_high', 'education_low', 'WHO_grade', 'PA_diagnosis', 'age_T0']]
X_socio_test.rename(columns={'ID_code':'ID'}, inplace=True)

#make ID str
X_socio_test['ID'] = X_socio_test['ID'].astype(str)
X_test_data['ID'] = X_test_data['ID'].astype(str)

#merge socio features
X_test_merge = X_test_data.merge(X_socio_test, on='ID', how='inner')

#dict for data
data = {'BERT':x_data, 'Predictors':X_socio, 'BERT+Pred.':X_ds}
data_test = {'BERT':X_test_data, 'Predictors':X_socio_test, 'BERT+Pred.':X_test_merge}

# make dictionary for all scores
scores = {'Zsc_psychomsp_T0':{}, 'Zsc_reactime_T0':{}, 'Zsc_complexatt_T0':{}, 'Zsc_cognflex_T0':{},'Zsc_procspeed_T0':{},
           'Zsc_verbalmem_T0':{}, 'Zsc_vismem_T0':{}, 'Zsc_motorspeed_T0':{},'Zsc_EF_T0':{}}

# loop over z scores in y file
for (column, y) in y_data.iteritems():
    if column in scores.keys():
        y_test = y_test_data.loc[:, column]
        # all indexes that are nan save to list
        iy = y[y.isna()].index.tolist()
        y = y.to_numpy()
        # also for test
        iy_test = y_test[y_test.isna()].index.tolist()
        y_test = y_test.to_numpy()
        # remove instances that are nan in dataset
        y = np.delete(y, iy, axis=0)
        y_test = np.delete(y_test, iy_test, axis=0)
        print(column)
        for name in data:
            # remove ID column and make np array
            X = data[name].loc[:, data[name].columns != 'ID'].to_numpy()
            X_test = data_test[name].loc[:, data_test[name].columns != 'ID'].to_numpy()
            # remove instances that are nan in dataset
            X = np.delete(X, iy, axis=0)
            X_test = np.delete(X_test, iy_test, axis=0)
            # configure the cross-validation procedure
            cv_inner = KFold(n_splits=3, shuffle=True, random_state=2022)
            model = linear_model.Lars(normalize=False)
            if name == 'Predictors':
                # define search space
                param_grid = {
                    'model__n_nonzero_coefs': [2, 3, 4, 5]
                }
            else:
                # define search space
                param_grid = {
                    'model__n_nonzero_coefs': [10, 15, 20, 25, 30, 35, 40, 45, 50]
                }
            # define pipelines
            pipe = Pipeline([('scaler', StandardScaler()), ('model', model)])
            # define search
            Lars_search = GridSearchCV(pipe, param_grid, scoring='r2', cv=cv_inner, refit=True)
            # execute search
            Lars = Lars_search.fit(X, y)
            # get the best performing model fit on the whole training set
            best_Lars = Lars.best_estimator_
            # evaluate model on the hold out dataset
            y_Lars = best_Lars.predict(X_test)
            # evaluate the model
            score_Lars = r2_score(y_test, y_Lars)
            # store the result
            scores[column][name]=score_Lars
            print(name)
            print(Lars.best_estimator_.get_params())
print(scores)
# save in json files
Save_json.save(json_obj=scores, name='final')