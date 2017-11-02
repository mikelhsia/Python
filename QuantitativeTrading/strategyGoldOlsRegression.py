
"""
Strategy name: GLD（黄金的现货价格）与GDX（採金企业的ETF）的配对交易
Date: 2017/11/01
Author: Michael Hsia
Description: 展示如何将数据分成训练集和测试集。我们将回测一个配对交易策略，在训练集上优化参数，在测试集上观察效果
			 黄金多头和黄金ETF空头所形成的差价呈均值回归，透过训练集上的回归分析可得出两者之间的对冲比率
"""
import datetime
from matplotlib.dates import date2num
import numpy as np
import ts2numpy as ts2np

"""
Tips:

Terms:
前视偏差
数据迁就偏差
样本含量
样本外测试: 训练集，测试集
"""

"""
Main function
Description: 
"""
def main():

	goldTicker = "601899"
	goldETFTicker = "518880"
	begDate = "2017-01-01"
	endDate = "2017-11-01"
	goldArray = ts2np.ts2numpy_dohcl(goldTicker, begDate, endDate)
	goldETFArray = ts2np.ts2numpy_dohcl(goldETFTicker, begDate, endDate)

	# print(goldArray)
	# print(goldETFArray)


if __name__ == "__main__":
	main()
