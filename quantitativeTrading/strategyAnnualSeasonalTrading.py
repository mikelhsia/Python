"""
Strategy name: 跨年季节趋势策略
Date: 2017/11/29
Author: Michael Hsia
Description: 每个月买进去年本月业绩最好的股票，同时间卖空去年本月业绩最差的股票
"""
import numpy as np
import tushare as ts
import datetime
import pandas as pd

"""
Tips:

Terms:
"""

TESTING_FLAG = True
TESTING_SCOPE = 3

def main():

	if TESTING_FLAG:
		i = 0

	begDate = "2013-11-01"
	today = datetime.date.today()

	hs300Tickers = ts.get_hs300s()

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

	# 将日期index变成其中一个栏位
	tickerPriceWithDateTable = tickerPriceTable.reset_index()
	tickerPriceWithDateTable.iloc[:, 0] = tickerPriceWithDateTable.iloc[:, 0].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))

	# 找到月底几天的指数
	thisMonth = pd.DataFrame(tickerPriceWithDateTable.iloc[:-1, 0])
	nextMonth = pd.DataFrame(tickerPriceWithDateTable.iloc[1:, 0])

	print(type(nextMonth))
	print(type(nextMonth.iloc[0,0]))
	print(nextMonth)
	print(thisMonth)

	lastDays = thisMonth - nextMonth
	print(lastDays)
	# print(tickerPriceWithDateTable[lastDays])
	# monthEnds = tickerPriceTable[isLastTradingDayOfMonth(tickerPriceTable.index)]

if __name__ == "__main__":
	main()
