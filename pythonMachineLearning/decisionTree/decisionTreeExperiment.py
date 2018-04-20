import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from sklearn import tree
import pydotplus
from sklearn.externals.six import StringIO
from IPython.display import Image, display
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from itertools import product

import matplotlib.pyplot as plt

import tushare as ts

target = ['change_rate_quant']
predictors = ['PCF', 'turnover_ratio', 'PE_rate', 'PB_rate', 'PS_rate', 'pmi', 'pmi_rate', 'leading_idx_rate', 'M1_rate',
              'M2_rate', 'CPI_rate', 'GDP_rate', 'LOAN6MONTH', 'LARGEFINANCIAL', 'SMALLFINANCIAL', 'dcg', 'URUR']

def get_bins (srs, frac= []):
    arr = []

    if (frac == []) :
        raise Exception('frac array is empty. Please specify quantile detail');
    bn = srs.quantile([0.3, 0.7])
    arr = [pd.Series.min(srs)] + [bn.iloc[x] for x in range(pd.Series.count(bn))] + [pd.Series.max(srs)]
    return arr

df = ts.get_hist_data('600848')

# TODO: Moving windows and rolling
df['change_rate'] = df['close'].pct_change()
cats = pd.cut(df['change_rate'], get_bins(df['change_rate'], [0.25, 0.75]))

# print(cats.values)
# print(cats.values.codes)
# print(cats.values.categories)

df['change_rate_quant'] = cats.values.codes
print(df['change_rate_quant'])
