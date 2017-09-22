import matplotlib.pyplot as plt
import tushare as ts
import numpy as np
import datetime

choice = 0
if (__name__ == '__main__'):
	choice = input("""What kind of chart you would like to see?
	1. Comparing stock and market returns
	2. Understanding the time value money
	3. Candlesticks representation of IBM's daily price
	4. Graphical representation of two-year price movement
	So?   """)


if choice == '1':
	def ret_f(ticker, begDate, endDate):
		p = ts.get_hist_data(ticker, start=begDate, end=endDate)
		p = p.sort_index(axis='index')
		px = np.array(p.close[1:])
		py = np.array(p.close[:-1])
		return (px - py) / px


	myTicker = '600848'
	SHTicker = '000001'
	begDate = datetime.date(2017,1,1)
	endDate = datetime.date.today()

	ret1 = ret_f(myTicker, begDate.__str__(), endDate.__str__())
	ret2 = ret_f(SHTicker, begDate.__str__(), endDate.__str__())

	numberOfRows = min(len(ret1), len(ret2))

	itemNumber = range(numberOfRows)
	horizontalLine = np.zeros(numberOfRows)

	# s = np.ones(numberOfRows) * 2
	# plt.plot(itemNumber, ret1[0:numberOfRows], 'ro', s)
	# plt.plot(itemNumber, ret2[0:numberOfRows], 'bd', s)
	# plt.plot(itemNumber, horizontalLine, 'b', s)
	plt.plot(itemNumber, ret1[0:numberOfRows], 'ro')
	plt.plot(itemNumber, ret2[0:numberOfRows], 'bd')
	plt.plot(itemNumber, horizontalLine, 'b')

	plt.figtext(0.4, 0.8, "Red for stock, Blue for index")
	plt.xlim(1, numberOfRows)
	plt.title("Comparisons between stock and market return")
	plt.xlabel("Day")
	plt.ylabel("Returns")

	plt.show()

elif choice == '2':
	fig1 = plt.figure(facecolor='white')
	ax1 = plt.axes(frameon=True)
	ax1.set_frame_on(False)
	ax1.get_xaxis().tick_bottom()
	ax1.axes.get_yaxis().set_visible(False)

	x = range(0, 11, 2)
	x1 = range(len(x), 0, -1)
	y = [0] * len(x)

	plt.annotate("Today's value of $100 received today", xy=(0, 0), xytext=(2, 0.1), arrowprops=dict(facecolor='black', shrink=0.02))
	plt.annotate("Today's value of $100 received in 2 years", xy=(2, 0.0005), xytext=(3.5, 0.08), arrowprops=dict(facecolor='black', shrink=0.02))
	plt.annotate("received in 6 years", xy=(4, 0.00005), xytext=(5.3, 0.06), arrowprops=dict(facecolor='black', shrink=0.02))
	plt.annotate("received in 10 years", xy=(10, -0.00005), xytext=(4, -0.06), arrowprops=dict(facecolor='black', shrink=0.02))

	plt.xlim(-2, 12)

	s = [50 * 2.5 ** n for n in x1]
	plt.title("Time value of money")
	plt.xlabel("Time (number of years)")
	plt.scatter(x, y, s=s)

	plt.show()

elif choice == '3':
	from matplotlib.dates import DateFormatter, WeekdayLocator, HourLocator, DayLocator, MONDAY
	from matplotlib.pylab import date2num
	from matplotlib.finance import candlestick_ohlc, candlestick_ochl

	date1 = datetime.date(2017,8,1)
	date2 = datetime.date.today()
	ticker = '000001'

	mondays = WeekdayLocator(MONDAY)    # Major ticks on the mondays
	alldays = DayLocator()              # Minor ticks on the days
	weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
	dayFormatter = DateFormatter('%d')      # e.g., 12

	quotes = ts.get_hist_data(ticker, start=date1.__str__(), end=date2.__str__())
	quotes = quotes.sort_index(axis='index')

	# 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
	quoteList = []

	# Iterate over DataFrame rows as (index, Series) pairs.
	for dates, row in quotes.iterrows():
		# 将时间转换为数字
		date_time = datetime.datetime.strptime(dates, "%Y-%m-%d")
		t = date2num(date_time)
		open, high, close, low = row[:4]
		# datas = (t, open, close, high, low)
		datas = (t, open, high, low, close)
		quoteList.append(datas)


	if len(quotes) == 0:
		raise SystemExit
	fig, ax = plt.subplots()
	fig.subplots_adjust(bottom=0.2)
	ax.xaxis.set_major_locator(mondays)
	ax.xaxis.set_minor_locator(alldays)
	ax.xaxis.set_major_formatter(weekFormatter)
	ax.xaxis.set_minor_formatter(dayFormatter)

	# candlestick_ochl(ax, quoteList, width=0.6)
	candlestick_ohlc(ax, quoteList, width=0.6)

	ax.xaxis_date()
	ax.autoscale_view()
	plt.setp(plt.gca().get_xticklabels(), rotation=80, horizontalalignment='right')

	plt.figtext(0.35, 0.32, 'Black ==> Close > Open ')
	plt.figtext(0.35, 0.28, 'Red   ==> Close < Open ')
	plt.title('Candlesticks for Shanghai index from 08/01/2017 to today')
	plt.ylabel('Price')
	plt.xlabel('Date')

	plt.show()

elif choice == '4':
	from matplotlib.dates import DateFormatter, MonthLocator, WeekdayLocator, MONDAY
	from matplotlib.dates import date2num

	ticker = '000001'
	begDate = datetime.date(2017,1,1)
	endDate = datetime.datetime.today()
	months = MonthLocator(range(1,13), bymonthday=1, interval=3) # every 3rd month
	monthsFmt = DateFormatter("%b '%Y")
	mondays = WeekdayLocator(MONDAY)    # Major ticks on the mondays

	quotes = ts.get_hist_data(ticker, start=begDate.__str__(), end=endDate.__str__())

	if len(quotes) == 0:
		print("Found no data")
		raise SystemExit

	dates = []
	closes = []

	for date, row in quotes.iterrows():
		# 将时间转换为数字
		date_time = datetime.datetime.strptime(date, "%Y-%m-%d")
		t = (date2num(date_time))
		close = row[2]
		# datas = (t, open, close, high, low)
		dates.append(t)
		closes.append(close)

	fig, ax = plt.subplots()
	ax.plot_date(dates, closes, '-')
	ax.xaxis.set_major_locator(months)
	ax.xaxis.set_major_formatter(monthsFmt)
	ax.xaxis.set_minor_locator(mondays)
	ax.autoscale_view()
	ax.grid(True)           # Show grid
	# ax.grid(False)
	fig.autofmt_xdate()     # Format the x-axis ticker as date

	plt.show()
	pass
