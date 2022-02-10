##############################################################
#                                                            #
#    Niek Huijsmansen                                        #
#    Textmining medical notes for cognition                  #
#    Outlier Z score                                         #
#                                                            #
##############################################################

import scipy
import math
import numpy as np

# Class for outlier detection algorithms based on some distribution of the data. They
# all consider only single points per row (i.e. one column).
class OutlierDetection:

    # Finds outliers in the specified columns of datatable and removes outliers
    def chauvenet(self, data_table, col):
        # take only the column
        data = data_table[col]
        #remove nans
        data.dropna(inplace=True)
        # Taken partly from: https://www.astro.rug.nl/software/kapteyn/
        # Computer the mean and standard deviation.
        mean = data.mean()
        std = data.std()
        N = len(data.index)
        criterion = 1.0 / (2 * N)

        # Consider the deviation for the data points.
        deviation = abs(data - mean) / std

        # Express the upper and lower bounds.
        low = -deviation / math.sqrt(2)
        high = deviation / math.sqrt(2)
        mask = []

        # Pass all rows in the dataset.
        for i in data.index.tolist():
            # Determine the probability of observing the point
            prob = 1.0 - 0.5 * (scipy.special.erf(high.loc[i]) - scipy.special.erf(low.loc[i]))
            # And mark as an outlier when the probability is below our criterion.
            if prob < criterion:
                mask.append(i)
            else:
                continue
        print(data_table.loc[mask, col])
        data_table.loc[mask, col] = np.nan
        return data_table



