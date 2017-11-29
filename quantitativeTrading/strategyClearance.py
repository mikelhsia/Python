"""
Strategy name: 清仓策略
Date: 2017/11/30
Author: Michael Hsia
Description:
"""
import numpy as np
import ts2numpy as ts2np
import statsmodels.api as sm
import datetime

"""
Tips:

Terms:
"""

def main():
	hsIndex = ts2np.ts.get_hs300s()
	# print(hsIndex.code)
	print(hsIndex.name)
	# print(hsIndex.date)
	# print(hsIndex.weight)

	for ticker in hsIndex.code:
		begDate = "2016-11-01"
		endDate = str(datetime.date.today())
		ticketClosePrice = ts2np.ts2numpy_dohcl(ticker, begDate, endDate)
		print("{} - {} ~ {}".format(ticker, begDate, endDate))
	else:
		print("DONE!")
		# dataSet = np.array([goldArray[3], goldETFArray[3]])


if __name__ == '__main__':
	main()
