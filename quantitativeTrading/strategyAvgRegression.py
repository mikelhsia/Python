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
学术界一般沿用以下的思路对股票价格的"状态转换"进行建模（马尔科夫状态转换模型/隐马尔科夫模型）
1. 假设价格在两个（或多个）状态上的概率分布不同。最简单的情形，两个状态的价格都服从正态分布，但均值或标准差不同
2. 假设状态之间存在某种转移概率
3. 使用诸如最大似然估计这样的标准统计方法，通过拟合历史数据，来确定状态概率分布和转移概率的参数
4. 根据以上拟合模型，找出下一个时间的期望状态，更重要的是，找出股票的期望价格

拐点模型：输入所有可能预测拐点或状态转换变量，包括当前的波动率，最近一期收益，以及消费者信心指数，石油变化价格，债券价格变化等
宏观经济数据的变化等。

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
