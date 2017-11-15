"""
Strategy name: 凯利公式
Date: 2017/11/10
Author: Michael Hsia
Description:
"""
import numpy as np
import ts2numpy as ts2np
import datetime

"""
Tips:
1. 机构交易员不会交易任何一支价格低于5美元的股票。低价股票会增加总佣金成本（对于一定的资本，需要买进或卖出更多股票），还会有相对较高的买卖差价
2. 风险管理守则：目标是优化长期财富投资最大化
3. 凯利公式适用于连续金融的前提是收益率成正态分布
4. 可通过对历史最大单期亏损的简单回测，对于能承受的净值最大单期挫跌要做到心中有数
5. 如果能承受一天20%的净值亏损，可用的最大杠杆就是1，而半凯利公式杠杆高达1.26
6. 止损不一定是好的清仓策略。但若消息或是其他基本面原因（如公司业绩下降）导致价格波动，一般来说就算惯性状态
7. 凯利公式的用处: 
	1. 决定最优杠杆
	2. 根据不同策略的收益的协方差，决定不同策略之间的最优资本配置

Terms:
状态转换：指金融市场的结构或是宏观经济环境发生了巨变
行为金融：研究非理性金融决策
	1. 禀赋效应:只有价格比购买时高很多的情况下才愿意卖掉股票
	2. 安于现状偏差
	3. 厌恶亏损
	4. 代表性偏差：人们倾向于对近期经验赋予过多权重
"""

def main():
	oilStockLabel = 1
	bankStockLabel = 2
	retailStockLabel = 3
	tickers = ['601857', '601318', '300033']
	begDate = "2016-11-01"
	endDate = str(datetime.date.today())
	dataSet = None

	np.set_printoptions(threshold=10)   # Adjust print columns number to 10

	for ticker in tickers:
		ticketClosePrice = ts2np.ts2numpy_dohcl(ticker, begDate, endDate)
		if dataSet is None:
			# Actually we don't need the date
			# dataSet = np.array(ticketClosePrice[0])
			dataSet = np.array(ticketClosePrice[3])
		else:
			# dataSet = np.array([dataSet, ticketClosePrice[3]])
			dataSet = np.row_stack((dataSet, ticketClosePrice[3]))
	else:
		print("Done combining three stocks into one array!")
		# print(dataSet)

	# 收益率
	ret = np.array((dataSet[:,1:] - dataSet[:,:-1]) / dataSet[:,:-1])

	from numpy.matlib import repmat
	# 超频收益率：假设年无风险利率 4%
	excessRet = ret - repmat(0.04/252, len(ret), len(ret[0]))
	# print(excessRet)

	# 年平均超额收益率
	M = 252 * np.mean(excessRet, 1).reshape(3, 1)
	print(M)

	# 年协方差矩阵
	C = 252 * np.cov(excessRet)
	print(C)

	# 凯利最优杠杆
	# (a).T －－ 返回自身的转置
	# (b).H －－ 返回自身的共轭转置
	# (c).I －－ 返回自身的逆矩阵
	# (d).A －－ 返回自身数据的2维数组的一个视图
	F = np.matrix(C).I * M
	print("F:\n{}".format(F))


if __name__ == '__main__':
	main()
