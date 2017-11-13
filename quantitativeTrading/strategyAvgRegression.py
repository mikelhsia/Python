"""
Strategy name: 均值回归策略与惯性策略
Date: 2017/11/10
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
均值回归策略
惯性策略
"""

def main():
	hsIndex = ts2np.ts.get_hs300s()

	for ticker in hsIndex.code:
		begDate = "2016-11-01"
		endDate = str(datetime.date.today())
		# ticketClosePrice = ts2np.ts2numpy_dohcl(ticker, begDate, endDate)
		print("{} - {} ~ {}".format(ticker, begDate, endDate))
	else:
		print("DONE!")
		# dataSet = np.array([goldArray[3], goldETFArray[3]])


if __name__ == '__main__':
	main()
