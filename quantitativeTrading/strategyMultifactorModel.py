"""
Strategy name: 多因子模型分析
Date: 2017/11/19
Author: Michael Hsia
Description:
"""
import numpy as np
import tushare as ts
import datetime

"""
Tips:
使用回望交易日作为估计区间（训练集），以此来决定因子风险
回望期交易日为252天，因子5个
交易策略为：购买下一个交易日期望收益率最高的20只股票

Terms:
"""

topN = 20

def _getHS300Tickers():
	tickers = ts.get_hs300s()
	return tickers['code']

def main():

	hs300Tickers = _getHS300Tickers()

	# begDate = "2016-11-01"
	# endDate = str(datetime.date.today())
	# dataSet = None
	#
	# np.set_printoptions(threshold=10)   # Adjust print columns number to 10

	for ticker in hs300Tickers:
		print(ticker)

	# 	ticketClosePrice = ts2np.ts2numpy_dohcl(ticker, begDate, endDate)
	# 	if dataSet is None:
	# 		# Actually we don't need the date
	# 		# dataSet = np.array(ticketClosePrice[0])
	# 		dataSet = np.array(ticketClosePrice[3])
	# 	else:
	# 		# dataSet = np.array([dataSet, ticketClosePrice[3]])
	# 		dataSet = np.row_stack((dataSet, ticketClosePrice[3]))
	# else:
	# 	print("Done combining three stocks into one array!")
	# 	# print(dataSet)

	# 收益率
	# ret = np.array((dataSet[:, 1:] - dataSet[:, :-1]) / dataSet[:, :-1])


if __name__ == "__main__":
	main()