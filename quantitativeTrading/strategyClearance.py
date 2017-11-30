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
1. 策略的清仓信号主要为以下几种：
	1.1. 固定的持有期
	1.2. 目标价格和盈利上限
	1.3. 最新的建仓信号
	1.4. 止损价格
	1.5. 其他策略默认的清仓信号
2. Orstein-Uhlenbeck 公式来建立均值回归模型。用符号z(t)来表示股票配对的均值回归的差价：
	dz(t) = -theta(z(t) - priceMean)dt + dW
	dW: 某种高斯随机噪音

Terms:
惯性模型
最优持有期
半衰期：差价回归到最初偏离均值的一半所需要的期望时间为 ln(2) / theta
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
