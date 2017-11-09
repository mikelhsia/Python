
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
1. 若同时训练集和测试集上的夏普比率都很高，那么可以说此策略是无数据迁就偏差的。
2. 可以改不同的标准差阀值来调整出不同的夏普比率
3. 尚未考虑交易成本

Terms:
前视偏差
数据迁就偏差
样本含量
样本外测试: 训练集，测试集
"""
def main():
	"""
	Main function
	Description:
	"""

	goldTicker = "601899"
	goldETFTicker = "600824"
	begDate = "2016-11-01"
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
	# print("Spread: {}".format(spread))

	# 训练集平均差价
	spreadMean = np.mean(spread)
	# print("SpreadMean: {}".format(spreadMean))

	# 训练集差价标准差
	spreadStd = np.std(spread)
	# print("SpreadStd: {}".format(spreadStd))

	# 差价标准化 (用z-scores方法)
	zscore = (spread - spreadMean)/spreadStd
	# print("Zscore: {}".format(zscore))

	# 在组合价值向下跌破1.3倍标准差时，购买此差价组合
	longs = zscore <= -1.3
	# print("Longs: {}".format(longs))

	# 在组合价值上升超过.13倍标准差时，做空该差价组合
	shorts = zscore >= 1.3
	# print("Shorts: {}".format(shorts))

	# 当组合价值回到0.7倍标准差以内时，清仓
	exits = abs(zscore) <= 0.5
	# print("Exits: {}".format(exits))

	# 初始化头寸数组
	positions = np.zeros([len(zscore),2])
	# print(positions[0,:])

	# 多头入市
	from numpy.matlib import repmat
	positions[shorts, :] = repmat([-1, 1], len(shorts[shorts != False]), 1)

	# 空头入市
	positions[longs, :] = repmat([1, -1], len(longs[longs != False]), 1)
	# print(positions)

	# 清仓
	positions[exits, :] = repmat([0, 0], len(exits[exits == True]), 1)

	# 确保继续持仓，除非出现清仓信号
	# positions = fillMissingData(positions)

	# 合并两个价格序列 = dataSet
	dailyRet = (dataSet[:, 1:] - dataSet[:, :-1]) / dataSet[:, :-1]

	strategyRet = np.sum(dailyRet[:,:len(trainingSet[0,:])] * positions.T)
	# print(strategyRet)

	# 训练集的夏普比
	sharpeTrainSet = np.sqrt(252) * np.mean(dailyRet[:,:len(trainingSet[0,:])] * positions.T)/np.std(trainingSet)
	print(sharpeTrainSet)

	# 评测集的夏普比
	# Do everything again

	# 保存头寸文件以便检查数据先窥偏差

if __name__ == "__main__":
	main()
