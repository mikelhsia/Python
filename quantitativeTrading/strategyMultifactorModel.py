"""
Strategy name: 多因子模型分析
Date: 2017/11/19
Author: Michael Hsia
Description:
"""
import numpy as np
import ts2numpy as ts2np
import datetime

"""
Tips:

Terms:
"""

def main():
	oilStockLabel = 1
	bankStockLabel = 2
	retailStockLabel = 3
	tickers = ['601857', '601318', '300033']
	begDate = "2016-11-01"
	endDate = str(datetime.date.today())
	dataSet = None

	np.set_printoptions(threshold=10)   # Adjust print columns number to 10

	for ticker in tickers:
		ticketClosePrice = ts2np.ts2numpy_dohcl(ticker, begDate, endDate)
		if dataSet is None:
			# Actually we don't need the date
			# dataSet = np.array(ticketClosePrice[0])
			dataSet = np.array(ticketClosePrice[3])
		else:
			# dataSet = np.array([dataSet, ticketClosePrice[3]])
			dataSet = np.row_stack((dataSet, ticketClosePrice[3]))
	else:
		print("Done combining three stocks into one array!")
		# print(dataSet)

	# 收益率
	ret = np.array((dataSet[:,1:] - dataSet[:,:-1]) / dataSet[:,:-1]