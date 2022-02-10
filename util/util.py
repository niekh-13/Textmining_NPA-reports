##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    Visualizing                                             #
#                                                            #
##############################################################

import re
import scipy
import copy
import math
import numpy as np

# Not a class, just a bunch of useful functions.
def get_data_type(module_path):
    return re.search().group(0).strip('_')