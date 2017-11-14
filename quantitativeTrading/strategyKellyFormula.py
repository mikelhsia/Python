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
	ticker1 = '601857'
	ticker2 = '601318'
	ticker3 = '300033'

	# for ticker in hsIndex.code:
	# 	begDate = "2016-11-01"
	# 	endDate = str(datetime.date.today())
	# 	ticketClosePrice = ts2np.ts2numpy_dohcl(ticker, begDate, endDate)
	# 	print("{} - {} ~ {}".format(ticker, begDate, endDate))
	# else:
	# 	print("DONE!")
	# 	dataSet = np.array([goldArray[3], goldETFArray[3]])


if __name__ == '__main__':
	main()
