

"""
Strategy name: 计算纯多头策略和市场中性策略的夏普比率
Date: 2017/10/29
Author: Michael Hsia
"""
import datetime
from matplotlib.dates import date2num
import tushare as ts
import numpy as np

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


"""
Main function
"""
for value in range(30):
	myTicker = "300018"
	begDate = datetime.date(2017, 5, 1)
	endDate = datetime.date.today()

	quote = ts.get_hist_data(str(int(myTicker)+value), start=begDate.__str__(), end=endDate.__str__())
	quote = quote.sort_index(axis='index')

	if len(quote) == 0:
		print("Found no data")
		raise SystemExit

	dates = []
	opens = []
	highs = []
	closes = []
	lows = []

	dates, opens, highs, closes, lows = ts2mpf_dohcl(quote)

	dates = np.array(dates)
	opens = np.array(opens)
	highs = np.array(highs)
	closes = np.array(closes)
	lows = np.array(lows)

	dailyRet = (closes[2:]-closes[:-2])/closes[:-2]
	# 假设无风险利率是0.04, 每年252个交易日, 计算超额收益率
	excessRet = dailyRet-0.04/252

	sharpeRatio = np.sqrt(252)*np.mean(excessRet)/np.std(excessRet)

	print("The sharpe ratio of stock {} is: {}".format(str(int(myTicker)+value), sharpeRatio))
	print("Adding market neutral strategy short side...")

	shortTicker = "399006"
	shortQuote = ts.get_hist_data(shortTicker, start=begDate.__str__(), end=endDate.__str__())
	shortQuote = shortQuote.sort_index(axis='index')

	if len(shortQuote) == 0:
		print("Found no data")
		raise SystemExit

	shortDates = []
	shortOpens = []
	shortHighs = []
	shortCloses = []
	shortLows = []

	shortDates, shortOpens, shortHighs, shortCloses, shortLows = ts2mpf_dohcl(quote)

	shortDates = np.array(shortDates)
	shortOpens = np.array(shortOpens)
	shortHighs = np.array(shortHighs)
	shortCloses = np.array(shortCloses)
	shortLows = np.array(shortLows)

	dailyEntRet = (shortCloses[2:]-shortCloses[:-2])/shortCloses[:-2]

	# 日净收益率 (除以2是因为使用了两倍的资金)
	netRet = (dailyRet - dailyEntRet) / 2

	netSharpeRatio = np.sqrt(252) * np.mean(dailyEntRet) / np.std(dailyEntRet)

	print("Then the neutral strategy sharpe ratio is: {}".format(netSharpeRatio))
	print("============================")
