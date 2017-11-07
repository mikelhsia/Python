
"""
Strategy name: GLD（黄金的现货价格）与GDX（採金企业的ETF）的配对交易
Date: 2017/11/01
Author: Michael Hsia
Description: 展示如何将数据分成训练集和测试集。我们将回测一个配对交易策略，在训练集上优化参数，在测试集上观察效果
			 黄金多头和黄金ETF空头所形成的差价呈均值回归，透过训练集上的回归分析可得出两者之间的对冲比率
"""
import numpy as np
import ts2numpy as ts2np
import statsmodels.api as sm

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
	goldETFTicker = "600824"
	begDate = "2017-01-01"
	endDate = "2017-11-01"
	goldArray = ts2np.ts2numpy_dohcl(goldTicker, begDate, endDate)
	goldETFArray = ts2np.ts2numpy_dohcl(goldETFTicker, begDate, endDate)

	# print(len(goldArray[1]))
	# print(goldETFArray)
	dataSet = np.array([goldArray[3], goldETFArray[3]])

	# print(dataSet)

	trainingSet, testSet = np.hsplit(dataSet, 2)

	# print("Training Set:\n {}".format(trainingSet[1,:]))
	# print("Test Set:\n {}".format(testSet))

	y = trainingSet[0,:]
	x = trainingSet[1,:]
	X = sm.add_constant(x)
	model = sm.OLS(y, X)
	results = model.fit()

	# print("Result params:\n {}".format(results.params))
	# print("Result summary:\n {}".format(results.summary()))

	# 差价 = y - mx
	spread = trainingSet[0, :] - results.params[1] * trainingSet[1, :]
	# print("\t{}".format(trainingSet[0, 0]))
	# print(" - \t{}".format(results.params[1]))
	# print(" * \t{}".format(trainingSet[1,0]))
	# print("-------------------------")
	# print("{}".format(spread[0]))

	# 训练集平均差价
	spreadMean = np.mean(spread)

	# 训练集差价标准差
	spreadStd = np.std(spread)

	# 差价标准化 (用z-scores方法)
	zscore = (spread - spreadMean)/spreadStd

	# 在组合价值向下跌破两倍标准差时，购买此差价组合
	longs = zscore <= -2

	# 在组合价值上升超过两倍标准差时，做空该差价组合
	shorts = zscore >= 2

	# 当组合价值回到一倍标准差以内时，清仓
	exits = abs(zscore) <= 1

	# 初始化头寸数组
	positions = np.zeros(len(goldArray[3]))

	# 多头入市

	# 空头入市

	# 清仓

	# 确保继续持仓，除非出现清仓信号

	# 合并两个价格序列

	# 训练集的夏普比

	# 评测集的夏普比

	# 保存头寸文件以便检查数据先窥偏差

if __name__ == "__main__":
	main()
