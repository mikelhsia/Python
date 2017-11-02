
"""
Package Name:
Date: 2017/31/01
Author: Michael Hsia
Description:
"""
import datetime
from matplotlib.dates import date2num
import tushare as ts
import numpy as np


def ts2numpy_all(ticker: str, begDate: str, endDate: str):
	"""

	:param ticker: 6 digits
	:param begDate: Format = "2017-05-01"
	:param endDate: Format = "2017-05-01"
	:return:
	"""

	# TODO: To be completed
	quotes = ts.get_hist_data(ticker, start=begDate, end=endDate)
	quotes = quotes.sort_index(axis='index')

	if len(quotes) == 0:
		print("Found no data")
		raise SystemExit

	_quoteList = []

	# Iterate over DataFrame rows as (index, Series) pairs.
	for dates, row in quotes.iterrows():
		# 将时间转换为数字
		date_time = datetime.datetime.strptime(dates, "%Y-%m-%d")
		opened, high, closed, low = row[:4]
		data = (date_time, opened, high, low, closed)
		_quoteList.append(data)

	return np.array(_quoteList)

def ts2numpy_dohcl(ticker: str, begDate: str, endDate: str):

	"""

	:param ticker: 6 digits
	:param begDate: Format = "2017-05-01"
	:param endDate: Format = "2017-05-01"
	:return:
	"""
	quotes = ts.get_hist_data(ticker, start=begDate, end=endDate)
	quotes = quotes.sort_index(axis='index')

	if len(quotes) == 0:
		print("Found no data")
		raise SystemExit

	_dates = []
	_opens = []
	_closes = []
	_highs = []
	_lows = []

	# Iterate over DataFrame rows as (index, Series) pairs.
	for date, row in quotes.iterrows():
		# 将时间转换为数字
		date_time = datetime.datetime.strptime(date, "%Y-%m-%d")
		opened, high, closed, low = row[:4]
		_dates.append(date_time)
		_opens.append(opened)
		_highs.append(high)
		_closes.append(closed)
		_lows.append(low)

	return np.array(_dates), np.array(_opens), np.array(_highs), np.array(_closes), np.array(_lows)
