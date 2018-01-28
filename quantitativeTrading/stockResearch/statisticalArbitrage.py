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

list = ['600028.XSHG', '600104.XSHG', '601800.XSHG', '600704.XSHG', '000651.XSHE', '600011.XSHG', '600029.XSHG',
 '600741.XSHG', '600688.XSHG', '600068.XSHG', '601633.XSHG', '600585.XSHG', '600900.XSHG', '000625.XSHE',
 '600221.XSHG', '000876.XSHE', '600795.XSHG', '600023.XSHG', '601006.XSHG', '600886.XSHG', '600089.XSHG',
 '600066.XSHG', '600383.XSHG', '002202.XSHE', '001979.XSHE', '002081.XSHE', '000402.XSHE', '000069.XSHE',
 '600208.XSHG', '000776.XSHE', '600352.XSHG', '600177.XSHG', '601872.XSHG', '000623.XSHE', '600649.XSHG', '600674.XSHG']

for security in list:
    if 'portfolio' not in dir():
        portfolio = pd.DataFrame(ts.get_hist_data(security[:6], start='2017-01-01', end='2018-01-01')['close'])
    else:
        portfolio[security[:6]] = ts.get_hist_data(security[:6], start='2017-01-01', end='2018-01-01')['close']

sns.heatmap(portfolio.corr())
sns.clustermap(portfolio.corr())