"""
Strategy name: 季节性交易策略
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
TESTING_SCOPE = 3


def main():

	oneWayTransCost = 0.0005    # 5bp one way transaction cost

	begDate = "2013-11-01"
	today = datetime.date.today()

	hs300Tickers = ts.get_hs300s()
	if TESTING_FLAG:
		i = 0

	for ticker in hs300Tickers['code']:

		hisPrice = ts.get_hist_data(ticker, begDate, today.__str__())

		if 'tickerPriceTable' not in locals().keys():
			tickerPriceTable = pd.DataFrame(hisPrice['close'].rename(ticker), index=hisPrice.index)
		else:
			tickerPriceTable = pd.concat([tickerPriceTable, hisPrice['close'].rename(ticker)], axis=1)

		if TESTING_FLAG:
			i += 1
			if i > TESTING_SCOPE:
				# print(tickerPriceTable)
				break

	dateIndex = pd.DataFrame(tickerPriceTable.index, index=tickerPriceTable.index)
	years = dateIndex.applymap(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").year)
	years = years.iloc[:, 0].rename('years')
	months = dateIndex.applymap(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").month)
	months = months.iloc[:, 0].rename('months')
	nextDayYear = dateIndex.applymap(lambda x: (datetime.datetime.strptime(x, "%Y-%m-%d") + datetime.timedelta(days=1)).year)
	nextDayYear = nextDayYear.iloc[:, 0].rename('nextDayYear')
	nextDayMonth = dateIndex.applymap(lambda x: (datetime.datetime.strptime(x, "%Y-%m-%d") + datetime.timedelta(days=1)).month)
	nextDayMonth = nextDayMonth.iloc[:, 0].rename('nextDayMonth')

	dateTable = pd.concat([years, months, nextDayYear, nextDayMonth], axis=1)
	# print(dateTable)
	# print(type(dateTable))

	lastDayOfDec = dateTable[(dateTable['months'] == 12) & (dateTable['nextDayMonth'] == 1)]
	# 用where：
	# The where method is an application of the if-then idiom. For each element in the calling DataFrame,
	# if cond is True the element is used; otherwise the corresponding element from the DataFrame other is used
	# lastDayOfDec = dateTable.where((dateTable['months'] == 12) & (dateTable['nextDayMonth'] == 1))
	lastDayOfJan = dateTable[(dateTable['months'] == 1) & (dateTable['nextDayMonth'] == 2)]
	# print(lastDayOfDec)

	# 由于lastDayOfDec 从第一年开始，也就是代表在第一年开始执行策略的时候，并没有前一年的股价完整资料
	lastDayOfDec.loc[0, :] = np.NaN


if __name__ == "__main__":
	main()
