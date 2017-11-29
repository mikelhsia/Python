"""
Strategy name: 多因子模型分析
Date: 2017/11/19
Author: Michael Hsia
Description:
"""
import numpy as np
import tushare as ts
import datetime
import pandas as pd
from numpy.matlib import repmat
import statsmodels.api as sm

"""
Tips:
使用回望交易日作为估计区间（训练集），以此来决定因子风险
回望期交易日为252天，因子5个
交易策略为：购买下一个交易日期望收益率最高的20只股票

Terms:
"""
TESTING_FLAG = True
TESTING_SCOPE = 10

topN = 20
lookback = 30		# 回望期
numFactors = 5      # 因子5个

def _getHS300Tickers():
	tickers = ts.get_hs300s()
	return tickers['code']

def smartCov(m):
	goodStock = m.dropna(axis=0, how="any")

	# 移去均值
	xc = goodStock - repmat(goodStock.mean(axis=0).T, len(goodStock.values), 1)

	# 回传协方差矩阵
	return xc.corr()

def main():

	hs300Tickers = _getHS300Tickers()

	begDate = "2016-11-01"
	endDate = datetime.datetime.timestamp(datetime.datetime.today())

	np.set_printoptions(threshold=10)   # Adjust print columns number to 10
	if TESTING_FLAG:
		i = 0

	for ticker in hs300Tickers:

		hisPrice = ts.get_hist_data(ticker, begDate, datetime.datetime.fromtimestamp(endDate).__str__())

		'''
		Another way of implementing this
			try:
				print('Found: {0}'.format())
			except NameError:
				print('Not found')
			else:
		'''
		if 'tickerPriceTable' not in locals().keys():
			tickerPriceTable = pd.DataFrame(hisPrice['close'].rename(ticker), index=hisPrice.index)
		else:
			tickerPriceTable = pd.concat([tickerPriceTable, hisPrice['close'].rename(ticker)], axis=1)

		if TESTING_FLAG:
			i += 1
			if i > TESTING_SCOPE:
				print(tickerPriceTable)
				break


	# 建立全0的position table
	positionTable = pd.DataFrame(np.zeros(shape=(len(tickerPriceTable.index), len(tickerPriceTable.columns))),
		                        index=tickerPriceTable.index,
		                        columns=tickerPriceTable.columns)

	dailyRet = pd.DataFrame((tickerPriceTable.values[1:,:] - tickerPriceTable.values[:-1,:]) / tickerPriceTable.values[:-1,:], columns=tickerPriceTable.columns)

	for d in range(lookback+1, len(tickerPriceTable.index)):
		# R 的列是不同的观测现象
		R = dailyRet.iloc[(d - lookback + 1):d,:]

		# 不考虑所有收益率有缺失的股票
		RnoNA = R.dropna(axis=1, how='all')

		# 移除均值
		avgRnoNa = RnoNA.mean(axis=0)
		Rfinal = RnoNA - repmat(avgRnoNa.T, len(RnoNA.values), 1)

		# 计算不同股票收益率的协方差矩阵
		covR = smartCov(Rfinal)
		print("covR: {}".format(covR))

		# X是因子风险矩阵，B是因子收益率的方差
		# 用covR的特征值作为X的列向量
		[X, B] = np.linalg.eig(covR)

		# 保留的因子数为numFactors
		X = sm.add_constant(B[:, :B.shape[0] - numFactors])
		model = sm.OLS(Rfinal.iloc[:,-1], X)
		results = model.fit()

		# b 是从时间t-1到t的因子收益率
		b = results.params[1]

		# Rexp 是假设因子收益率保持常数时，下一个时间段的期望收益率
		Rexp = avgRnoNa + X * b

		pd.DataFrame.sort_index(Rexp, ascending=True)

		# 做空期望收益率最低的50只股票
		positionTable[d, Rexp.iloc[1:topN]] = -1

		# 做多期望收益率最大的50只股票
		positionTable[d, Rexp.iloc[-topN+1:]] = 1

		# 计算交易策略的每日收益率
		ret = pd.DataFrame.sum(matlab.backshift(1, positionTable) * dailyRet, 2)

		# 计算交易策略的年华收益率
		avgRet = pd.DataFrame.mean(ret) * 252

		if TESTING_FLAG:
			# print("RnoNA: \n{}".format(RnoNA))
			# print("avgRnoNA: \n{}".format(avgRnoNa))
			print("Rfinal: \n{}".format(Rfinal))
			break

		print("Daily Return : \n{}".format(ret))
		print("Annual Return : \n{}".format(avgRet))


if __name__ == "__main__":
	main()
