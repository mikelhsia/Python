import matplotlib.pyplot as plt
import tushare as ts
import numpy as np
import pandas as pd
import datetime

from matplotlib.pylab import date2num

def ts2mpf_all(quotes):
	quoteList = []

	# Iterate over DataFrame rows as (index, Series) pairs.
	for dates, row in quotes.iterrows():
		# 将时间转换为数字
		date_time = datetime.datetime.strptime(dates, "%Y-%m-%d")
		t = date2num(date_time)
		open, high, close, low = row[:4]
		datas = (t, open, high, low, close)
		quoteList.append(datas)

	return quoteList

def ts2mpf_dohcl(quotes):
	dates = []
	opens = []
	closes = []
	highs = []
	lows = []
	# Iterate over DataFrame rows as (index, Series) pairs.
	for date, row in quotes.iterrows():
		# 将时间转换为数字
		date_time = datetime.datetime.strptime(date, "%Y-%m-%d")
		t = date2num(date_time)
		open, high, close, low = row[:4]
		dates.append(t)
		opens.append(open)
		highs.append(high)
		closes.append(close)
		lows.append(low)

	return dates, opens, highs, closes, lows

choice = 0
if (__name__ == '__main__'):
	choice = input("""What kind of chart you would like to see?
	1. Comparing stock and market returns
	2. Understanding the time value money (and save to file)
	3. Candlesticks representation of IBM's daily price
	4. Graphical representation of two-year price movement
	5. Shanghai index's intra-day graphical representations
	6. Presenting both closing price and trading volume
	7. Adding mathematical formulae to our graph
	8. Adding simple images to our graphs
	9. Performance comparisons among stocks
	10. Comparing return versus volatility for several stocks
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
	from matplotlib.pylab import savefig

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

	savefig('/Users/tsuyuhsia/Desktop')

elif choice == '3':
	from matplotlib.dates import DateFormatter, WeekdayLocator, HourLocator, DayLocator, MONDAY
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

	quoteList = ts2mpf_all(quotes)

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

	ticker = '000001'
	begDate = datetime.date(2017,1,1)
	endDate = datetime.datetime.today()
	months = MonthLocator(range(1,13), bymonthday=1, interval=3) # every 3rd month
	monthsFmt = DateFormatter("%b '%Y")
	mondays = WeekdayLocator(MONDAY)    # Major ticks on the mondays

	quotes = ts.get_hist_data(ticker, start=begDate.__str__(), end=endDate.__str__())
	quotes = quotes.sort_index(axis='index')

	if len(quotes) == 0:
		print("Found no data")
		raise SystemExit

	dates = []
	opens = []
	highs = []
	closes = []
	lows = []

	dates, opens, highs, closes, lows = ts2mpf_dohcl(quotes)

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

elif choice == '5':
	ticker = 'AAPL'
	path = 'http://www.google.com/finance/getprices?q=ttt&i=60&p=3d&f=d,o,h,l,c,v'
	p = np.array(pd.read_csv(path.replace('ttt', ticker), skiprows=7, header=None))

	date = []

	for i in np.arange(0, len(p)):
		if p[i][0][0] == 'a':
			t = datetime.datetime.fromtimestamp(int(p[i][0].replace('a', '')))
			date.append(t)
		else:
			date.append(t+datetime.timedelta(minutes = int(p[i][0])))

	final = pd.DataFrame(p, index=date)
	final.columns = ['a', 'Open', 'High', 'Low', 'Close', 'Vol']
	del final['a']

	x = final.index
	y = final.Close

	plt.title('Intraday price pattern for AAPL')
	plt.xlabel('Price of stock')
	plt.ylabel('Intro-day price pattern')

	plt.plot(x, y)

	plt.show()

elif choice == '6':
	ticker = '000001'
	begDate = datetime.date(2016,1,1)
	endDate = datetime.datetime.today()

	quotes = ts.get_hist_data(ticker, start=begDate.__str__(), end=endDate.__str__())
	quotes = quotes.sort_index(axis='index')

	quoteList = ts2mpf_all(quotes)

	# Not really working since plotfile needs file handler as first argument
	# plt.plotfile(quoteList, (0, 6, 5))

	# plt.show()

elif choice == '7':
	import matplotlib.mathtext as mt
	import matplotlib as mpl

	mpl.rc('image', origin='upper')
	parser = mt.MathTextParser("Bitmap")

	r'$\left[\left\lfloor\frac{5}{\frac{\left(3\right)}{4}} y\right)\right]$'
	rgba1, depth1 = parser.to_rgba(r'$d_2=\frac{ln(S_0/K)+(r-\sigma^2/2)T}{\sigma\sqrt{T}}=d_1-\sigma\sqrt{T}$', color='black', fontsize=12, dpi=200)
	rgba2, depth2 = parser.to_rgba(r'$d_1=\frac{ln(S_0/K)+(r+\sigma^2/2)T}{\sigma\sqrt{T}}$', color='blue', fontsize=12, dpi=200)
	rgba3, depth3 = parser.to_rgba(r'$c=S_0N(d_1)- Ke^{-rT}N(d_2)$', color='red', fontsize=14, dpi=200)

	fig = plt.figure()
	fig.figimage(rgba1.astype(float)/255., 100, 100)
	fig.figimage(rgba2.astype(float)/255., 100, 200)
	fig.figimage(rgba3.astype(float)/255., 100, 300)

	plt.show()

elif choice == '8':
	# cbook module is a collection of utility functions and classes.
	# Many of them are from the Python cookbook
	import matplotlib.cbook as cbook
	imageFile = cbook.get_sample_data('/Users/tsuyuhsia/Desktop/1.png')
	img = plt.imread(imageFile)

	plt.imshow(img)
	# plt.axis('off')
	plt.autoscale(True)

	plt.show()

elif choice == '9':

	plt.rcdefaults()        # 恢复 rc 的默认设置

	tickers = ('000001', '000002', '000008', '000009', '000010')
	begDate = datetime.date(2017, 1, 1)
	endDate = datetime.datetime.today()

	performance = []

	for t in tickers:
		quotes = ts.get_hist_data(t, start=begDate.__str__(), end=endDate.__str__())
		quotes = quotes.sort_index(axis='index')
		quotesX = np.array(quotes.close[1:])
		quotesY = np.array(quotes.close[:-1])
		logRet = np.log(quotesX / quotesY)

		performance.append(np.exp(sum(logRet))-1)

	y_pos = np.arange(len(tickers))

	plt.barh(y_pos, performance, left=0, alpha=0.3)
	plt.yticks(y_pos, tickers)
	plt.xlabel('Annual Returns ')
	plt.title('Performance comparisons (Annual Return)')

	plt.show()

elif choice == '10':

	plt.rcdefaults()

	tickers = ('000001', '000002', '000008', '000009', '000010')
	begDate = datetime.date(2017, 1, 1).__str__()
	endDate = datetime.datetime.today().__str__()

	def retVol(ticker):
		quotes = ts.get_hist_data(ticker, start=begDate, end=endDate)
		quotes = quotes.sort_index(axis='index')
		quotesX = np.array(quotes.close[1:])
		quotesY = np.array(quotes.close[:-1])
		logRet = np.log(quotesX / quotesY)

		return (np.exp(sum(logRet)) - 1, np.std(logRet))

	ret = []
	vol = []

	for t in tickers:
		r, v =retVol(t)
		ret.append(r)
		vol.append(v*np.sqrt(252))

	labels = ['{0}'.format(i) for i in tickers]
	plt.xlabel('Volatility (annualized)')
	plt.ylabel('Annual Return')
	plt.title('Return vs. Volatility')
	plt.subplots_adjust(bottom=0.1)
	color = np.array([0.18, 0.96, 0.75, 0.3, 0.9])

	plt.scatter(vol, ret, marker='o', c=color, s=1000, cmap=plt.get_cmap('Spectral'))

	for label, x, y in zip(labels, vol, ret):
		plt.annotate(label, xy=(x,y), xytext=(-20, 20), textcoords='offset points',
	            ha='right', va='bottom',
	            bbox=dict(boxstyle='round, pad=0.5', fc = 'yellow', alpha=0.5),
	            arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=0'))

	plt.show()
	pass
