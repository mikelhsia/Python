import matplotlib.pyplot as plt
import tushare as ts
import numpy as np
import datetime

choice = 0
if (__name__ == '__main__'):
	choice = input("""What kind of chart you would like to see?
	1. Comparing stock and market returns
	2. Understanding the time value money
	So?""")


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
