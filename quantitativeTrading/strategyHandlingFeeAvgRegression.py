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
import tushare as ts

import matplotlib.pyplot as plt

"""
Tips:
0. 重要指标：夏普比率，跌挫
1. 任何夏普比率低于1的策略都不适合单独使用
2. 几乎每月都实现盈利的策略，其年化夏普比率通常都大于2
3. 几乎每天都盈利的策略，其年华夏普比率通常都大于3
4. 应当去寻找被大多数机构投资者忽略的策略。例如：交易频繁而容量很低的策略，每天只交易少数股票的策略

Terms:
滑价
存活偏差
分拆及股息调整后的历史数据库
"""

print(ts.get_hs300s())
print(ts.get_zz500s())
print(ts.get_sz50s())