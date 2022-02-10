##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    t-SNE                                                   #
#                                                            #
##############################################################

# Import the relevant packages
import numpy as np
import pandas as pd
from util.VisualizeData import VisualizeDataset
import os
from pathlib import Path
from sklearn.manifold import TSNE
import pyreadstat

DataViz = VisualizeDataset(__file__)

# input files and directories
file_mpnet = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TRAIN/multi_mpnet_embeddings.csv')
file_bert = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TRAIN/dutch_bert_embeddings.csv')
file_y = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TRAIN/y_train.sav')

#import y dataframe with labels
y_train, meta = pyreadstat.read_sav(file_y, apply_value_formats=True)

### MPNet ###
#import mpnet file as pandas dataframe
X_train_m = pd.read_csv(file_mpnet)

#to numpy for PCA en tSNE
X_m = X_train_m.loc[:, X_train_m.columns != 'ID'].to_numpy()
# calculate tSNE for 2 componenets
x_tSNE_m = TSNE(n_components=2, learning_rate='auto', init='random').fit_transform(X_m)
DATA_tSNE_m = pd.DataFrame(x_tSNE_m, columns=['tsne1', 'tsne2'])

#plot for tSNE
DATA_tSNE_m['sex'] = y_train['sex']
DataViz.tSNE_m(DATA_tSNE_m)


### BERT ###
#import mpnet file as pandas dataframe
X_train_b = pd.read_csv(file_bert)

#to numpy for PCA en tSNE
X_b = X_train_b.loc[:, X_train_b.columns != 'ID'].to_numpy()
# calculate tSNE for 2 componenets
x_tSNE_b = TSNE(n_components=2, learning_rate='auto', init='random', verbose=3).fit_transform(X_b)
DATA_tSNE_b = pd.DataFrame(x_tSNE_b, columns=['tsne1', 'tsne2'])

#plot for tSNE
DATA_tSNE_b['sex'] = y_train['sex']
DataViz.tSNE_b(DATA_tSNE_b)
