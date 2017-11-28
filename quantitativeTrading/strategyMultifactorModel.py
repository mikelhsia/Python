"""
Strategy name: 多因子模型分析
Date: 2017/11/19
Author: Michael Hsia
Description:
"""
import numpy as np
import tushare as ts
import datetime
import pandas as pd
from numpy.matlib import repmat

"""
Tips:
使用回望交易日作为估计区间（训练集），以此来决定因子风险
回望期交易日为252天，因子5个
交易策略为：购买下一个交易日期望收益率最高的20只股票

Terms:
"""
TESTING_FLAG = True
TESTING_SCOPE = 10

topN = 20

def _getHS300Tickers():
	tickers = ts.get_hs300s()
	return tickers['code']

def smartCov(m):
	print("{} {}".format(len(m), len(m.columns)))
	y = np.matrix(np.repeat(np.NaN, len(m))).repeat(len(m), axis=0)
	xc = np.repeat(np.NaN, len(m.columns))

	# TODO [smartCov]: Not correct yet. Still need to be recalculated
	goodStock = m.dropna(axis=0, how="any")
	goodStockmean = goodStock.mean(axis=0)
	goodStockRep = repmat(goodStock.mean(axis=0).T, len(m.values), 1)
	xc = goodStock - repmat(goodStock.mean(axis=0).T, len(m.values), 1)
	return

def main():

	hs300Tickers = _getHS300Tickers()

	begDate = "2016-11-01"
	endDate = datetime.datetime.timestamp(datetime.datetime.today())
	lookback = 30		# 回望期

	np.set_printoptions(threshold=10)   # Adjust print columns number to 10
	if TESTING_FLAG:
		i = 0

	for ticker in hs300Tickers:

		hisPrice = ts.get_hist_data(ticker, begDate, datetime.datetime.fromtimestamp(endDate).__str__())

		'''
		Another way of implementing this
			try:
				print('Found: {0}'.format())
			except NameError:
				print('Not found')
			else:
		'''
		if 'tickerPriceTable' not in locals().keys():
			tickerPriceTable = pd.DataFrame(hisPrice['close'].rename(ticker), index=hisPrice.index)
		else:
			tickerPriceTable = pd.concat([tickerPriceTable, hisPrice['close'].rename(ticker)], axis=1)

		if TESTING_FLAG:
			i += 1
			if i > TESTING_SCOPE:
				print(tickerPriceTable)
				break


	# 建立全0的position table
	positionTable = pd.DataFrame(np.zeros(shape=(len(tickerPriceTable.index), len(tickerPriceTable.columns))), 
		                        index=tickerPriceTable.index, 
		                        columns=tickerPriceTable.columns)

	dailyRet = pd.DataFrame((tickerPriceTable.values[1:,:] - tickerPriceTable.values[:-1,:]) / tickerPriceTable.values[:-1,:], columns=tickerPriceTable.columns)

	for d in range(lookback+1, len(tickerPriceTable.index)):
		# R 的列是不同的观测现象
		R = dailyRet.iloc[(d - lookback + 1):d,:]

		# 不考虑所有收益率有缺失的股票
		RnoNA = R.dropna(axis=0, how='any')

		# 移除均值
		avgRnoNa = RnoNA.mean(axis=0)
		Rfinal = RnoNA - repmat(avgRnoNa.T, len(RnoNA.values), 1)

		# 计算不同股票收益率的协方差矩阵

		if TESTING_FLAG:
			# print("RnoNA: \n{}".format(RnoNA))
			# print("avgRnoNA: \n{}".format(avgRnoNa))
			print("Rfinal: \n{}".format(Rfinal))
			break

	smartCov(Rfinal)

	# 收益率
	# ret = np.array((dataSet[:, 1:] - dataSet[:, :-1]) / dataSet[:, :-1])


if __name__ == "__main__":
	main()