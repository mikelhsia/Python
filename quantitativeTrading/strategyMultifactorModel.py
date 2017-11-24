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

"""
Tips:
使用回望交易日作为估计区间（训练集），以此来决定因子风险
回望期交易日为252天，因子5个
交易策略为：购买下一个交易日期望收益率最高的20只股票

Terms:
"""
TESTING_FLAG = True

topN = 20

def _getHS300Tickers():
	tickers = ts.get_hs300s()
	return tickers['code']

def main():

	hs300Tickers = _getHS300Tickers()

	begDate = "2016-11-01"
	endDate = datetime.datetime.timestamp(datetime.datetime.today())
	lookback = 30		# 回望期

	# np.set_printoptions(threshold=10)   # Adjust print columns number to 10
	if TESTING_FLAG == True:
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

		if TESTING_FLAG == True:
			i += 1
			if i > 4:
				break

	print(tickerPriceTable)

	# 建立全0的position table
	positionTable = pd.DataFrame(np.zeros(shape=(len(tickerPriceTable.index), len(tickerPriceTable.columns))), 
		                        index=tickerPriceTable.index, 
		                        columns=tickerPriceTable.columns)

	dailyRet = pd.DataFrame((tickerPriceTable.values[1:,:] - tickerPriceTable.values[:-1,:]) / tickerPriceTable.values[:-1,:], columns=tickerPriceTable.columns)

	for d in range(lookback+1, len(tickerPriceTable.index)):
		# R 的列是不同的观测现象
		R = dailyRet.ix[(d - lookback + 1):d,:]

		if TESTING_FLAG == True:
			print(R)
			break

	# 收益率
	# ret = np.array((dataSet[:, 1:] - dataSet[:, :-1]) / dataSet[:, :-1])


if __name__ == "__main__":
	main()