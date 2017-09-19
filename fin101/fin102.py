import matplotlib.pyplot as plt
import tushare as ts
import numpy as np
import datetime


if (__name__ == '__main__'):
	choice = input("""What kind of chart you would like to see?
	1. Comparing stock and market returns""")

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
plt.title("Comparisons betwen stock and market return")
plt.xlabel("Day")
plt.ylabel("Returns")

plt.show()