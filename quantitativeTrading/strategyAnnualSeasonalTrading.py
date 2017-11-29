"""
Strategy name: 跨年季节趋势策略
Date: 2017/11/29
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

Terms:
"""
TESTING_FLAG = True
TESTING_SCOPE = 10

def _getHS300Tickers():
	tickers = ts.get_hs300s()
	return tickers['code']

def main():

	hs300Tickers = _getHS300Tickers()

	begDate = "2016-11-01"
	endDate = datetime.datetime.timestamp(datetime.datetime.today())

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


if __name__ == "__main__":
	main()
