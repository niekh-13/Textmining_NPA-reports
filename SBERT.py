##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    Stopwords removal                                       #
#                                                            #
##############################################################
# Import the relevant packages
import pandas as pd
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer


# input files and directories
DATA_PATH = Path('/home/niek/Documents/Textmining_minor_intern_VU_ETZ/Textmining_ETZ/TRAIN')
OUTPUT_dutch = Path('dutch_bert_embeddings.csv')
OUTPUT_multi = Path('multi_mpnet_embeddings.csv')
# OUTPUT_extra = Path('multi_mpnet_embeddings.csv')

#load in tokenizer and model from BERTJE
model_dutch = SentenceTransformer("jegorkitskerkin/bert-base-dutch-cased-snli")
# model_dutch._first_module().max_seq_length = 512
model_multi = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")
# model_multi._first_module().max_seq_length = 512
# model_extra = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
# model_extra._first_module().max_seq_length = 512
# model_small = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 ')
# model_small._first_module().max_seq_length = 512

#import input file as pandas dataframe
file = os.path.join(DATA_PATH, 'X_train.csv')
file = os.path.abspath(file)
DATA = pd.read_csv(file)

###Word embeddings###
#dutch
X_train_dutch = model_dutch.encode(list(DATA['T0_obs_truth']), convert_to_numpy=True)
#multi
X_train_multi = model_multi.encode(list(DATA['T0_obs_truth']), convert_to_numpy=True)
#extra multi
# X_train_extra = model_extra.encode(list(DATA['T0_obs_truth']), convert_to_numpy=True, normalize_embeddings=True)

#drop text column
DATA.drop(['T0_obs_truth'], inplace=True, axis=1)

#concat to IDS
DATA_dutch = pd.concat([DATA, pd.DataFrame(X_train_dutch)], axis=1)
DATA_multi = pd.concat([DATA, pd.DataFrame(X_train_multi)], axis=1)
# DATA_extra = pd.concat([DATA, pd.DataFrame(X_train_extra)], axis=1)


#export top csv file
DATA_dutch.to_csv(DATA_PATH / OUTPUT_dutch, index=False)
DATA_multi.to_csv(DATA_PATH / OUTPUT_multi, index=False)
# DATA_extra.to_csv(DATA_PATH / OUTPUT_extra, index=False)

