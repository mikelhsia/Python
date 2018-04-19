
"""
Strategy name: 计算纯多头策略和市场中性策略的夏普比率, 计算最大挫跌和最长挫跌期
Date: 2017/10/29
Author: Michael Hsia
"""
import datetime
from matplotlib.dates import date2num
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt

"""
Tips:
0. 重要指标：夏普比率，跌挫
1. 任何夏普比率低于1的策略都不适合单独使用
2. 几乎每月都实现盈利的策略，其年化夏普比率通常都大于2
3. 几乎每天都盈利的策略，其年华夏普比率通常都大于3
4. 应当去寻找被大多数机构投资者忽略的策略。例如：交易频繁而容量很低的策略，每天只交易少数股票的策略

Terms:
滑价
存活偏差
分拆及股息调整后的历史数据库
"""
"""
Tips:
1. 继续使用多空市场中性策略，来计算最大挫跌和最长挫跌期
2. 第一步：在每日收盘时计算"高水位线"。即到这一天为止策略的最大收益率
3. 用累计收益率曲线和净值曲线计算高水位线是一样的。因为净值 = 初始投资额 * （1 + 累计收益率）


Terms:
挫跌
最大挫跌
最长挫跌期
"""

# Test whether the mean daily returns from Shanghai Index is zero:
def ts2mpf_all(quotes):
	_quoteList = []

	# Iterate over DataFrame rows as (index, Series) pairs.
	for dates, row in quotes.iterrows():
		# 将时间转换为数字
		date_time = datetime.datetime.strptime(dates, "%Y-%m-%d")
		t = date2num(date_time)
		opened, high, closed, low = row[:4]
		data = (t, opened, high, low, closed)
		_quoteList.append(data)

	return _quoteList


def ts2mpf_dohcl(quotes):
	_dates = []
	_opens = []
	_closes = []
	_highs = []
	_lows = []
	# Iterate over DataFrame rows as (index, Series) pairs.
	for date, row in quotes.iterrows():
		# 将时间转换为数字
		date_time = datetime.datetime.strptime(date, "%Y-%m-%d")
		t = date2num(date_time)
		opened, high, closed, low = row[:4]
		_dates.append(t)
		_opens.append(opened)
		_highs.append(high)
		_closes.append(closed)
		_lows.append(low)

	return _dates, _opens, _highs, _closes, _lows


def calculateMaxDD(cumRet):
	# 在累计收益率的基础上计算最大挫跌和最长挫跌期
	# 将高水位线初始化为0, 挫跌初始化为0, 最长挫跌期初始化为0
	highWaterMark = np.zeros(np.size(cumRet))
	drawDown = np.zeros(np.size(cumRet))
	drawDownDuration = np.zeros(np.size(cumRet))

	for t in range(1, len(cumRet)):
		highWaterMark[t] = max(highWaterMark[t - 1], cumRet[t])
		# 计算每日挫跌(相对于高水位)
		drawDown[t] = (1 + highWaterMark[t]) / (1 + cumRet[t]) - 1

		if drawDown[t] == 0:
			drawDownDuration[t] = 0
		else:
			drawDownDuration[t] = drawDownDuration[t - 1] + 1

	x = [value for value in range(len(cumRet))]
	y = cumRet

	plt.title(u'300018\'s MaxDD and MaxDDD')
	plt.xlabel(u'Number of days')
	plt.ylabel(u'Accumulated return (%)')

	plt.plot(x, y)
	plt.show()

	# return maxDD, maxDDD
	return max(drawDown), max(drawDownDuration)


"""
Main function
Description: 
"""
def _main():
	# FIXME: 最后存货偏差的没找到。像停牌很久的啊，没资料的啊，都没有过滤掉
	myTicker = "300018"
	begDate = datetime.date(2017, 5, 1)
	endDate = datetime.date.today()

	quote = ts.get_hist_data(myTicker, start=begDate.__str__(), end=endDate.__str__())
	quote = quote.sort_index(axis='index')

	if len(quote) == 0:
		print("Found no data")
		raise SystemExit

	dates, opens, highs, closes, lows = ts2mpf_dohcl(quote)

	dates = np.array(dates)
	opens = np.array(opens)
	highs = np.array(highs)
	closes = np.array(closes)
	lows = np.array(lows)

	dailyRet = (closes[2: ] - closes[:-2] ) / closes[:-2]
	# 假设无风险利率是0.04, 每年252个交易日, 计算超额收益率
	excessRet = dailyRet - 0.04 / 252

	sharpeRatio = np.sqrt(252) * np.mean(excessRet) / np.std(excessRet)

	print("The sharpe ratio of stock {} is: {}".format(myTicker, sharpeRatio))
	print("Adding market neutral strategy short side...")

	shortTicker = "159915"
	shortQuote = ts.get_hist_data(shortTicker, start=begDate.__str__(), end=endDate.__str__())
	shortQuote = shortQuote.sort_index(axis='index')

	if len(shortQuote) == 0:
		print("Found no data")
		raise SystemExit

	shortDates, shortOpens, shortHighs, shortCloses, shortLows = ts2mpf_dohcl(shortQuote)

	shortDates = np.array(shortDates)
	shortOpens = np.array(shortOpens)
	shortHighs = np.array(shortHighs)
	shortCloses = np.array(shortCloses)
	shortLows = np.array(shortLows)

	dailyEntRet = (shortCloses[2:] - shortCloses[:-2]) / shortCloses[:-2]

	# 日净收益率 (除以2是因为使用了两倍的资金)
	netRet = (dailyRet - dailyEntRet) / 2

	netSharpeRatio = np.sqrt(252) * np.mean(netRet) / np.std(netRet)

	print("Then the neutral strategy sharpe ratio is: {}".format(netSharpeRatio))

	cumRet = np.cumprod(1 + netRet) - 1
	maxDD, maxDDD = calculateMaxDD(cumRet)
	print("MaxDD: {}, MaxDDD: {}".format(maxDD, maxDDD))
	print("============================")


if __name__ == "__main__":
	_main()
