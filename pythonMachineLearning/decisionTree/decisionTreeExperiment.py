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

response = ['change_rate_quant']
predictors = ['PCF', 'turnover_ratio', 'PE_rate', 'PB_rate', 'PS_rate', 'pmi', 'pmi_rate', 'leading_idx_rate', 'M1_rate',
              'M2_rate', 'CPI_rate', 'GDP_rate', 'LOAN6MONTH', 'LARGEFINANCIAL', 'SMALLFINANCIAL', 'dcg', 'URUR']

df = ts.get_hist_data('600848')

# TODO: Moving windows and rolling
df['change_rate'] = df['close'].pct_change()
bin = df['change_rate'].quantile([0.3, 0.7])
bins = [pd.Series.min(df['change_rate']), bin.iloc[0], bin.iloc[1], pd.Series.max(df['change_rate'])]
cats = pd.cut(df['change_rate'], bins)

# print(cats.values)
# print(cats.values.codes)
# print(cats.values.categories)

df['change_rate_qunat'] = cats.values.codes
