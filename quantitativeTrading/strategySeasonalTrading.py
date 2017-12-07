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
TESTING_SCOPE = 8

TOPN = 10

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

	tickerPriceTable = pd.concat([tickerPriceTable, years, months, nextDayYear, nextDayMonth], join='inner', axis=1)
	# print("Ticker price: \n{}".format(tickerPriceTable))

	lastDayOfDec = tickerPriceTable[(tickerPriceTable['months'] == 12) & (tickerPriceTable['nextDayMonth'] == 1)]
	# 用where：
	# The where method is an application of the if-then idiom. For each element in the calling DataFrame,
	# if cond is True the element is used; otherwise the corresponding element from the DataFrame other is used
	# lastDayOfDec = dateTable.where((dateTable['months'] == 12) & (dateTable['nextDayMonth'] == 1))
	lastDayOfJan = tickerPriceTable[(tickerPriceTable['months'] == 1) & (tickerPriceTable['nextDayMonth'] == 2)]
	# print(lastDayOfDec)

	# 由于lastDayOfDec 从第一年开始，也就是代表在第一年开始执行策略的时候，并没有前一年的股价完整资料
	lastDayOfDec.loc[0, :] = np.NaN

	# 年末指数
	eoy = tickerPriceTable[tickerPriceTable['years'] == tickerPriceTable['nextDayYear']]
	# print("EOY:\n{}".format(eoy))

	# 上一个指数不是年末的
	eoy.iloc[-1, :] = np.NaN

	# 确保eoy日期和lastDayOfDec日期匹配
	# assert(all(tday(eoy) == tday(lastDayOfDec)))

	# 年收益率
	annRet = pd.DataFrame((eoy.values[1:,:] - eoy.values[:-1,:]) / eoy.values[:-1,:], columns=eoy.columns)
	# print(annRet)

	# 年收益率
	# janRet = pd.DataFrame((lastDayOfJan.values[1:,:] - lastDayOfDec.values[:-1,:]) / lastDayOfDec.values[:-1,:], columns=eoy.columns)
	# print(annRet)

	annRet = annRet.drop(labels=["years", "months", "nextDayYear", "nextDayMonth"], axis=1)
	# print(annRet)

	# How matlab strategy to sort all stocks, but don't think it applys to python
	# for index, stock in enumerate(annRet):
	# 	# print("{}, {}".format(index, stock))
	# 	annRet = annRet.sort_values(by=stock.__str__(), axis=1, ascending=True)
	# 	print(annRet[stock])
	annAvgRet = annRet.mean(axis=0, skipna=True, numeric_only=True)
	# print("{}:\n{}".format(type(annAvgRet), annAvgRet))
	annAvgRet = annAvgRet.sort_values(axis=0, ascending=False)
	# print("{}:\n{}".format(type(annAvgRet), annAvgRet))
	topN = annAvgRet.head(n=TOPN)
	# print("TopN:\n{}".format(annAvgRet.head(n=TOPN)))

	# 组合收益率
	# portRet = (smartMean(janRet(sortidx(:topN))) - smartMean(janRet(sortidx(end-topN:)))) / 2 - 2 * oneWayTransCost
	# print("Last holding date: {}\n Portfolio return: {}".format(tday(lastDayOfDec+1), portRet))

if __name__ == "__main__":
	main()
