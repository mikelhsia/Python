"""
Strategy name: 交易成本与均值回归模型
Date: 2017/11/10
Author: Michael Hsia
Description: MIT的Amir Khandani 和 Andrew Lo提出了以下模型：
			 "买入前一日交易日日收益最差的股票，并卖空前一交易日日收益最好的股票"
			 假定每笔交易成本为5个基点时，策略业绩如何变化
			 （此处的一笔交易指的是一笔买入或一笔卖出，并不是一笔来回交易）
"""
import numpy as np
import ts2numpy as ts2np
import statsmodels.api as sm
import datetime

"""
Tips:
1. 通常S&P500指数成份股是最好用来做回测的数据，因为他的流动性是最好的。

Terms:
"""

def main():
	hsIndex = ts2np.ts.get_hs300s()
	# print(hsIndex.code)
	# print(hsIndex.name)
	# print(hsIndex.date)
	# print(hsIndex.weight)

	for ticker in hsIndex.code:
		begDate = "2016-11-01"
		endDate = str(datetime.date.today())
		# goldArray = ts2np.ts2numpy_dohcl(goldTicker, begDate, endDate)
		print("{} - {} ~ {}".format(ticker, begDate, endDate))
	else:
		print("DONE!")
		# dataSet = np.array([goldArray[3], goldETFArray[3]])


if __name__ == '__main__':
	main()