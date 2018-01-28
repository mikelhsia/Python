"""
Strategy name: 统计套利 Statistical Arbitrage
Date: 2018/01/27
Author: Michael Hsia
Description:
统计套利就是其中之一：这个策略的概念最早产生于Morgan Stanley。当时的做法也被称为配对交易。
实际上就是使用统计数据选取一堆历史价格走势相似的股票。当两只股票之间的价格差距变大，超出一定阀值之后，
就分别做多和做空这两只股票，依靠该价格差在随后的时间里回归到正常水平来获取收益。
"""
import pandas as pd
import numpy as np
import datetime
import tushare as ts
import seaborn as sns

# 获取所有沪深300的股票里pe_ratio不为0的股票
stocks300SH = get_index_stocks('000300.XSHG')
stocks300SHDf = get_fundamentals(
	query(valuation, income, balance).filter(valuation.code.in_(stocks300SH), valuation.pe_ratio > 0),
	statDate='2017q3').sort('pe_ratio_lyr', ascending=False)

# stocks300SHDf = get_fundamentals(query(valuation, income, balance).filter(valuation.code.in_(stocks300SH), valuation.pe_ratio >0)).sort('pe_ratio', ascending=False)

# 股票公司名字的DF
stocks300SH = pd.DataFrame(stocks300SH, columns=['code'])
stocks300SH['name'] = stocks300SH.code
stocks300SH.name = stocks300SH.code.apply(lambda x: get_security_info(x).display_name)

# Merge 名称的DF
stocks300SHDf = pd.merge(stocks300SHDf, stocks300SH, on='code', how='inner')

# 取pe_ratio最低的25%
SH300PeRatioQuarter = stocks300SHDf.pe_ratio_lyr.quantile(0.25)
stocks300SHDfPortfolio = stocks300SHDf[
	(stocks300SHDf.pe_ratio_lyr < SH300PeRatioQuarter) & (stocks300SHDf.pe_ratio_lyr > 0)].sort('pe_ratio_lyr',
                                                                                                ascending=False)
stocks300SHDfPortfolio

# 取debt_to_equity_ratio最低的上0%
debtToEquityRatioDf = stocks300SHDfPortfolio['total_liability'] / stocks300SHDfPortfolio['total_sheet_owner_equities']
stocks300SHDfPortfolio = stocks300SHDfPortfolio[debtToEquityRatioDf < debtToEquityRatioDf.quantile()]

# 重新将名字排到id后面
cols = stocks300SHDfPortfolio.columns.tolist()
cols = [cols[1]] + [cols[-1]] + cols[2:-1]
stocks300SHDfPortfolio = stocks300SHDfPortfolio[cols]
stocks300SHDfPortfolio.reset_index(drop=True, inplace=True)

# operating revenue 较高的拥有较高的交易执行权
stocks300SHDfPortfolio = stocks300SHDfPortfolio.sort('total_operating_revenue', ascending=False)


del portfolio

for security in stocks300SHDfPortfolio.code.tolist():
    if 'portfolio' not in dir():
        portfolio = pd.DataFrame(ts.get_hist_data(security[:6], start='2017-01-01', end='2018-01-01')['close'])
    else:
        portfolio[security[:6]] = ts.get_hist_data(security[:6], start='2017-01-01', end='2018-01-01')['close']

sns.heatmap(portfolio.corr())
sns.clustermap(portfolio.corr())