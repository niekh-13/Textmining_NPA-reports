##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    stopword removal                                        #
#                                                            #
##############################################################
#import relevant packages
import re
import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class stopword_removal:

    def __init__(self, DATA):
        self.DATA = DATA

    def tokenize(self):
        for column in self.DATA.columns:
            if "obs" in column:
                self.DATA[column] = self.DATA[column].apply(word_tokenize)
        data = self.DATA
        return data

    def removal_stopwords(self):
        stop_words = set(stopwords.words('dutch'))
        for column in self.tokenize():
            if 'obs' in column:
                self.DATA[column] = self.DATA[column].apply(lambda row: [w.lower() for w in row if not w.lower() in stop_words])
        return self.DATA

