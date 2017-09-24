import numpy as np
import pandas as pd

# Used to generate an index array
dates = pd.date_range('20130101', periods=5)
np.random.seed(12345)
x = pd.DataFrame(np.random.rand(5, 2), index=dates, columns=('A', 'B'))

# Offers the properties of those two columns, such as mean and standard deviation.
print(x.describe())

x1 = pd.Series([0.1, 0.02, -0.03, np.nan, 0.130, 0.125])
fill = np.mean(x1)
np.round(fill, 4)
y = x1.fillna(fill)

del dates, x, x1, fill, y

'''
Ordinary Least Square (OLS) regression is a method for 
estimating the unknown parameters in a linear regression model.
It minimizes the sum of squared vertical distances between the observed 
values and the values predicted by the linear approximation.

Assume that we have the following equation where y is an n by 1 vector (array),
 and x is an n by (m+1) matrix, a return matrix (n by m), plus a vector that 
 contains 1 only. N is the number of observations, and m is the number of 
 independent variables:
'''

import statsmodels.api as sm

y = [1, 2, 3, 4, 2, 3, 4]
x = range(1, 8)
x = sm.add_constant(x)
results = sm.OLS(y, x).fit()

# The last line prints the parameters only
print(results.params)