"""
Strategy name: 如何构造协整度高（均值回归）的股票配对
Date: 2017/11/16
Author: Michael Hsia
Description: 如果做多一个证券的同时以正确的比例做空另一个同行业证券，组合（或差价）有时是一个平稳序列。
			平稳的时间序列是均值回归策略的绝佳候选。本文来检验两个价格序列是否协整，以及如何找到最优的对冲比率。
"""
import numpy as np
import ts2numpy as ts2np
import datetime
import statsmodels.tsa.stattools as ts
import statsmodels.api as sm


"""
Tips:
协整检验的主要方法为ADF检验，python中可使用现成的工具statsmodels来实现adf检验
x = np.array([1, 2, 3, 4, 5, 6, 7])
result = ts.adfuller(x, 1)
print result 
(-2.6825663173365015, 0.077103947319183241, 0, 7 , 
	{'5%': -3.4775828571428571, '1%': -4.9386902332361515, '10%': -2.8438679591836733} ,
	15.971188911270618)

statsmodels.tsa.stattools.adfuller(x, maxlag=None, regression='c', autolag='AIC', store=False, regresults=False)[source]¶
x: 序列，一维数组
maxlag：差分次数
regresion:{c:只有常量， ct:有常量项和趋势项， ctt:有常量项、线性和二次趋势项， nc:无任何选项}
autolag:{aic or bic: default, then the number of lags is chosen to minimize the corresponding information criterium, None:use the maxlag, t-stat:based choice of maxlag. Starts with maxlag and drops a lag until the t-statistic on the last lag length is significant at the 95 % level.}

Terms:
协整检验
ADF检验
平稳时间序列
非平稳时间序列
"""

def main():

	goldIdx = 0
	goldETFIdx = 1
	goldTicker = "601899"
	goldETFTicker = "600824"
	begDate = "2016-11-01"
	endDate = "2017-11-01"
	goldArray = ts2np.ts2numpy_dohcl(goldTicker, begDate, endDate)
	goldETFArray = ts2np.ts2numpy_dohcl(goldETFTicker, begDate, endDate)

	dataSet = np.array([goldArray[3], goldETFArray[3]])

	'''
	用adf检验来检验序列时间平稳性。若t-统计量及临界值合理，则表示该两个时间序列是协整且平稳的。
	如此一来，做线性回归才有意义，不会发生伪性回归。
	
	协整性与correlation相关性并不相同
	'''
	# adfTest = ts.adfuller(dataSet)
	# print(adfTest, 2)
	return

	y = dataSet[goldIdx, :]
	x = dataSet[goldETFIdx, :]
	X = sm.add_constant(x)
	model = sm.OLS(y, X)
	results = model.fit()

	spread = dataSet[goldIdx, :] - results.params[1] * dataSet[goldETFIdx, :]
	spreadMean = np.mean(spread)
	spreadStd = np.std(spread)
	zscore = (spread - spreadMean) / spreadStd

	longs = zscore <= -1.3
	shorts = zscore >= 1.3
	exits = abs(zscore) <= 0.7

	# 初始化头寸数组
	positions = np.zeros([len(zscore), 2])

	from numpy.matlib import repmat
	positions[shorts, :] = repmat([-1, 1], len(shorts[shorts != False]), 1)
	positions[longs, :] = repmat([1, -1], len(longs[longs != False]), 1)
	positions[exits, :] = repmat([0, 0], len(exits[exits == True]), 1)

	dailyRet = (dataSet[:, 1:] - dataSet[:, :-1]) / dataSet[:, :-1]

	strategyRet = np.sum(dailyRet[:, ] * positions.T[:, :-1])
	print("Training SetStrategy Return: {}".format(strategyRet))

	sharpeSet = np.sqrt(252) * np.mean(dailyRet[:, ] * positions.T[:, :-1]) / np.std(dataSet)
	print("Training Set Sharpe Ratio: {}".format(sharpeSet))


if __name__ == '__main__':
	main()
