    #!/usr/bin/env python3
##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    PLSR                                                    #
#                                                            #
##############################################################

# Import the relevant packages
from util.VisualizeData import VisualizeDataset
from util.Save import Save
from sklearn import cross_decomposition
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
import pyreadstat
import os
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

#import y dataframe with labels
y_data, meta = pyreadstat.read_sav(file_y, apply_value_formats=False)
x_data = pd.read_csv(file_x)

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

#dict for data
data = {'bert':x_data, 'socio':X_socio, 'socio+bert':X_ds}

# loop over z scores in y file
for (column, y) in y_data.iteritems():
    if 'Zsc' in column and 'old' not in column:
        #all indexes that are nan save to list
        iy = y[y.isna()].index.tolist()
        y = y.to_numpy()
        #make dictionary for all scores
        scores = dict()
        for name in data:
            # remove ID column and make np array
            X = data[name].loc[:, data[name].columns != 'ID'].to_numpy() #
            # save results
            outer_results_PLSR = list()
            # Double loop cross validation
            for i in range(100):
                # configure the cross-validation procedure
                cv_outer = KFold(n_splits=3, shuffle=True, random_state=i)
                # split data on k3 fold and loop over k folds
                for train_ix, test_ix in cv_outer.split(X):
                    # remove nan values from y dataset
                    train_ix = np.setdiff1d(train_ix,iy)
                    test_ix = np.setdiff1d(test_ix,iy)
                    # split test and train data
                    X_train, X_test = X[train_ix], X[test_ix]
                    y_train, y_test = y[train_ix], y[test_ix]
                    # configure the cross-validation procedure
                    cv_inner = KFold(n_splits=10, shuffle=True, random_state=i)
                    # define the model
                    model = cross_decomposition.PLSRegression()
                    if name == 'socio':
                        # define search space
                        param_grid = {
                            'model__n_components': [2,3,4,5,6]
                        }
                    else:
                        # define search space
                        param_grid = {
                            'model__n_components': [2, 4, 6, 8, 16, 25, 32, 64, 80, 128]
                        }
                    # define pipelines
                    pipe = Pipeline([('scaler', StandardScaler()), ('model', model)])
                    # define search
                    PLSR_search = GridSearchCV(pipe, param_grid, scoring='r2', cv=cv_inner, refit=True)
                    # execute search
                    PLSR = PLSR_search.fit(X_train, y_train)
                    # get the best performing model fit on the whole training set
                    best_PLSR = PLSR.best_estimator_
                    # evaluate model on the hold out dataset
                    y_PLSR = best_PLSR.predict(X_test)
                    # evaluate the model
                    score_PLSR = r2_score(y_test, y_PLSR)
                    # store the result
                    outer_results_PLSR.append(score_PLSR)
            # store the results in the dictionary
            scores[name] = outer_results_PLSR
        # save in json files
        Save_json.save(json_obj=scores, name=column)
        # Create boxplot of scores per file
        DataViz.boxplot(scores, column)
        print(f'First Z score took: {str(datetime.now() - begin_time)}' )
print(f'Total time for PLSR was: {str(datetime.now() - begin_time)}')
