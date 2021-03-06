import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

############################################
# Used to generate an index array
dates = pd.date_range('20130101', periods=5)
np.random.seed(12345)
x = pd.DataFrame(np.random.rand(5, 2), index=dates, columns=('A', 'B'))

# Offers the properties of those two columns, such as mean and standard deviation.
print(x.describe())

x1 = pd.Series([0.1, 0.02, -0.03, np.nan, 0.130, 0.125])
fill = np.mean(x1)
np.round(fill, 4)
y = x1.fillna(fill)

del dates, x, x1, fill, y


'''
Ordinary Least Square (OLS) regression is a method for 
estimating the unknown parameters in a linear regression model.
It minimizes the sum of squared vertical distances between the observed 
values and the values predicted by the linear approximation.

Assume that we have the following equation where y is an n by 1 vector (array),
 and x is an n by (m+1) matrix, a return matrix (n by m), plus a vector that 
 contains 1 only. N is the number of observations, and m is the number of 
 independent variables:
'''


y = [1, 2, 3, 4, 2, 3, 4]
x = range(1, 8)
x = sm.add_constant(x)
results = sm.OLS(y, x).fit()

# The last line prints the parameters only
print(results.params)

del y, x, results


############################################
# 简单的数据模型分析
# y = 1 + 10x

# 虚构一组数据，数据量为100
nsample = 100

# 创建X的数据
x = np.linspace(0, 10, nsample)

# 加入常数项 1
X = sm.add_constant(x)

# 设置模型里的beta0 和 beta1
beta = np.array([1, 10])

# 然后加上误差项，所以生成一个长度为nsample的正态分布样本
e = np.random.normal(size=nsample)

# 生成 y(t)
# dot(a, b)[i,j,k,m] = sum(a[i,j,:] * b[k,:,m])
y = np.dot(X, beta) + e

# 在反映变量和回归变量上使用OLS
model = sm.OLS(y, X)

# fit 取结果, 再调取计算出的回归系数
results = model.fit()
print("results.params: {}".format(results.params))

# coef列就是计算出的回归系数
print("results.summary: {}".format(results.summary()))

# 将拟合结果画出来
# 先调用拟合结果的fittedvalues得到拟合的 y 值
y_fitted = results.fittedvalues

# matplotlib画图。设定图轴，图片大小为8x6
fig, ax = plt.subplots(figsize=(8, 6))

# 原数据
ax.plot(x, y, 'o', label='data')

# 拟合数据
ax.plot(x, y_fitted, 'r--.',label='OLS')

#注解
ax.legend(loc='best')
# ax.axis((-0.05, 2, -1, 25))

############################################
# y = B0 + B1x + B2x^2 + .... + Bnx^
# y = 1 + 0.1x + 10x^2
nsample = 100

x = np.linspace(0, 10, nsample)

# 创建一个 k×2 的 array，两列分别为 x1 和 x2。我们需要 x2 为 x1 的平方
X = np.column_stack((x, x**2))

# 使用 sm.add_constant() 在 array 上加入一列常项 1。
X = sm.add_constant(X)

# beta, e
beta = np.array([1, 0.1, 10])
e = np.random.normal(size=nsample)

y = np.dot(X, beta) + e
model = sm.OLS(y, X)
results = model.fit()
print(results.params)
print(results.summary())

############################################
# pd.read_csv()
# pd.read_clipboard()
# pd.read_table()
# pd.read_fwf()
# pd.read_hdf()
# pd.io()

# The Series() function included in the Pandas module would help us to generate time series.
# Data.Frame is used intensively in Python and other languages, such as R
x = pd.date_range('1/1/2013', periods=252)
date = pd.Series(np.random.randn(len(x)), index=x)

print(date)
del date

# import matplotlib.pyplot as plt
# import matplotlib.mathtext as mt
#
# parser = mt.MathTextParser("Bitmap")
#
# r'$\left[\left\lfloor\frac{5}{\frac{\left(3\right)}{4}} y\right)\right]$'
# rgba1, depth1 = parser.to_rgba(r'$d_2=\frac{ln(S_0/K)+(r-\sigma^2/2)T}{\sigma\sqrt{T}}=d_1-\sigma\sqrt{T}$', color='black', fontsize=12, dpi=200)
# rgba2, depth2 = parser.to_rgba(r'$d_1=\frac{ln(S_0/K)+(r+\sigma^2/2)T}{\sigma\sqrt{T}}$', color='blue', fontsize=12, dpi=200)
# rgba3, depth3 = parser.to_rgba(r'$c=S_0N(d_1)- Ke^{-rT}N(d_2)$', color='red', fontsize=14, dpi=200)
# rgba4, depth4 = parser.to_rgba(r'$R_{monthly}=\frac{P_{20}-P_0}{P_0}$', color='blue', fontsize=14, dpi=200)
# rgba5, depth5 = parser.to_rgba(r'$log\_return_{monthly}=log(\frac{P_{20}}{P_0})$', color='blue', fontsize=14, dpi=200)
# rgba6, depth6 = parser.to_rgba(r'$R_{montly}=exp(Log\_return))-1$', color='blue', fontsize=14, dpi=200)
#
# fig = plt.figure()
# fig.figimage(rgba4.astype(float)/255., 100, 100)
# fig.figimage(rgba5.astype(float)/255., 100, 200)
# fig.figimage(rgba6.astype(float)/255., 100, 300)
#
# plt.show()


# Merging datasets by date
# from matplotlib.finance import quotes_historical_yahoo_ochl
# import numpy as np
# import pandas as pd
# ticker='IBM'
# begdate=(2013,10,1)
# enddate=(2013,11,9)
# x = quotes_historical_yahoo(ticker, begdate, enddate, asobject=True, adjusted=True)
# k=x.date
# date=[]
# for i in range(0,size(x)):
#     date.append(''.join([k[i].strftime("%Y"),k[i].strftime("%m"),k[i].strftime("%d")]))
# x2=pd.DataFrame(x['aclose'],np.array(date,dtype=int64),columns=[ticker+'_adjClose'])
# ff=load('c:/temp/ffDaily.pickle')
# final=pd.merge(x2,ff,left_index=True,right_index=True)

########################################################################################################
# Student T-test and F-test
from scipy import stats
import tushare as ts
import datetime
from matplotlib.dates import date2num

np.random.seed(1235)
x = stats.norm.rvs(size=10000)
print("T-value   P-value  (two-tails")
print(stats.ttest_1samp(x, 5.0))
print(stats.ttest_1samp(x, 0))


# Test whether the mean daily returns from Shanghai Index is zero:
def ts2mpf_all(quotes):
	quoteList = []

	# Iterate over DataFrame rows as (index, Series) pairs.
	for dates, row in quotes.iterrows():
		# 将时间转换为数字
		date_time = datetime.datetime.strptime(dates, "%Y-%m-%d")
		t = date2num(date_time)
		open, high, close, low = row[:4]
		datas = (t, open, high, low, close)
		quoteList.append(datas)

	return quoteList


def ts2mpf_dohcl(quotes):
	dates = []
	opens = []
	closes = []
	highs = []
	lows = []
	# Iterate over DataFrame rows as (index, Series) pairs.
	for date, row in quotes.iterrows():
		# 将时间转换为数字
		date_time = datetime.datetime.strptime(date, "%Y-%m-%d")
		t = date2num(date_time)
		open, high, close, low = row[:4]
		dates.append(t)
		opens.append(open)
		highs.append(high)
		closes.append(close)
		lows.append(low)

	return dates, opens, highs, closes, lows


ticker = '000001'
begDate = datetime.date(2017, 1, 1).__str__()
endDate = datetime.datetime.today().__str__()

quotes = ts.get_hist_data(ticker, start=begDate, end=endDate)
quotes = quotes.sort_index(axis='index')
px = np.array(quotes.close[1:])
py = np.array(quotes.close[:-1])
ret = (px - py) / px

# From the previous results, we know that the average daily returns for Shanghai Index is 0.0011 percent.
# The T-value is 0.904 while the P-value is 0.3667. Thus, the mean is not statistically significantly different from zero.
print("Mean        T-value                                       P-value")
print(round(np.mean(ret), 5), stats.ttest_1samp(ret, 0))

########################################################################################################
'''
Next, we test whether two variances for IBM and DELL in 2013 are equal or not.
The function called sp.stats.bartlet performs Bartlett's test for equal variances
with a null hypothesis that all input samples are from populations with equal variances.
'''

import scipy as sp


def ret_f(ticker, begDate, endDate):
	p = ts.get_hist_data(ticker, start=begDate, end=endDate)
	p = p.sort_index(axis='index')
	px = np.array(p.close[1:])
	py = np.array(p.close[:-1])
	return (px - py) / px


x = ret_f('000001', '2017-01-01', '2017-09-01')
y = ret_f('000002', '2017-01-01', '2017-09-01')

# With a T-value of 15.1 and a P-value of 0.0001 percent, we conclude that these two stocks
# will have different variances for their daily stock returns in 2017 if we choose a significant level of 5 percent
print(sp.stats.bartlett(x, y))

# we use IBM's data to test the existence of the so-called January effect which states that stock returns
# in January are statistically different from those in other months
######
# from matplotlib.finance import quotes_historical_yahoo
# import numpy as np
# import scipy as sp
# from datetime import datetime
# ticker='IBM'
# begdate=(1962,1,1)
# enddate=(2013,11,22)
# x = quotes_historical_yahoo(ticker, begdate, enddate,asobject=True, adjusted=True)
# logret = log(x.aclose[1:]/x.aclose[:-1])
# date=[]
# d0=x.date
# for i in range(0,size(logret)):
#     t1=''.join([d0[i].strftime("%Y"),d0[i].strftime("%m"),"01"])
#     date.append(datetime.strptime(t1,"%Y%m%d"))
#     y=pd.DataFrame(logret,date,columns=['logret'])
#     retM=y.groupby(y.index).sum()
# ret_Jan=retM[retM.index.month==1]
# ret_others=retM[retM.index.month!=1]
# print(sp.stats.bartlett(ret_Jan.values,ret_others.values))(1.1592293088621082, 0.28162543233634485)
######
# Since the T-value is 1.16 and P-value is 0.28, we conclude that there is no January effect
# if we use IBM as an example and choose a 5 percent significant level.
# A word of caution: we should not generalize this result since it is based on just one stock.
#  In terms of the weekday effect, we could apply the same procedure to test its existence.


########################################################################################################
# Many useful applications
'''
In this section, we discuss many issues, such as 52-week high and low trading strategy
by taking a long position if today's price is close to the minimum price achieved in the past 52 weeks
and taking an opposite position if today's price is close to its 52-week high.
'''
########################################################################################################
# Not used
# from dateutil.relativedelta import relativedelta

ticker = '000001'
begDate = datetime.date(2017, 1, 1).__str__()
endDate = datetime.datetime.today().__str__()

p = ts.get_hist_data(ticker, start=begDate, end=endDate)
p = p.sort_index(axis='index')

x = p.close
y = list(p.close[:-1])
high = max(y)
low = min(y)

print("Today\t\t\tPrice\t\tHigh\t\tLow\t\t% from low")
print(x.index[-1], '\t\t', x[-1], '\t\t', high, '\t\t', low, '\t\t', round((x[-1] - low) / (high - low) * 100, 2))

########################################################################################################
# Roll's model to estimate spread (1984)
'''
Liquidity is defined as how quickly we can dispose of our asset without losing its intrinsic value.
Usually, we use spread to represent liquidity. However, we need high-frequency data to estimate spread.
Later in the chapter, we show how to estimate spread directly by using high-frequency data.
To measure spread indirectly based on daily observations, Roll (1984) shows that we can estimate it based on
the serial covariance in price changes as follows
'''

print("", end="\n________________\n")

import math
import matplotlib.mathtext as mt
import matplotlib as mpl

mpl.rc('image', origin='upper')
parser = mt.MathTextParser("Bitmap")

# P is the closing price of a stock on day t, ~P is the average share price in the estimation period
rgba1, depth1 = parser.to_rgba(r'$S=2\sqrt{-cov(\Delta P_t, \Delta P_{t-1})}$',
                               color='black', fontsize=12, dpi=200)
rgba2, depth2 = parser.to_rgba(r'$\%spread=\frac{s}{p}$', color='blue', fontsize=12,
                               dpi=200)

fig = plt.figure()
fig.figimage(rgba1.astype(float) / 255., 100, 100)
fig.figimage(rgba2.astype(float) / 255., 100, 200)

plt.show()
plt.clf()

ticker = '000001'
begDate = datetime.date(2017, 1, 1).__str__()
endDate = datetime.datetime.today().__str__()

data = ts.get_hist_data(ticker, start=begDate, end=endDate)
data = data.sort_index(axis='index')

p = data.close
d = np.diff(p)
cov_ = np.cov(d[:-1], d[1:])

if cov_[0, 1] < 0:
	print("Roll spread for ", ticker, " is ", round(2 * math.sqrt(-cov_[0, 1]), 3))
else:
	print("Cov is positive for ", ticker, " positive ", round(cov_[0, 1], 3))

'''
Thus, during that period, Roll's spread for IBM is 1.145. The major assumption for Roll's model is that the
covariance between  and  is negative. When its value is positive, Roll's model would fail. In a real world,
it is true for many cases. Usually, practitioners adopt two approaches: when the spread is negative, we just
ignore those cases or use other methods to estimate spread. The second approach is to add a negative sign in
front of a positive covariance.
'''

########################################################################################################
print("", end="\n________________\n")
mpl.rc('image', origin='upper')
parser = mt.MathTextParser("Bitmap")

'''
According to Amihud (2002), liquidity reflects the impact of order  ow on price. His illiquidity measure
is defined as follows:
Rt is the daily return at day t, Pt is closing price at t, and Vt is the daily dollar trading volume at t.
Since the illiquidity is the reciprocal of liquidity, the lower the illiquidity value, the higher the liquidity
of the underlying security.
'''
rgba1, depth1 = parser.to_rgba(r'$illiq_t = \frac{|R_t|}{P_t*V_t}$', color='black', fontsize=12, dpi=200)
fig = plt.figure()
fig.figimage(rgba1.astype(float) / 255., 100, 100)

plt.show()
plt.clf()

x = np.array([1, 2, 3], dtype='float')
y = np.array([2, 2, 4], dtype='float')
print("np.divide(x, y) = ", np.divide(x, y))

'''
In the following code, we estimate Amihud's illiquidity for IBM based on trading data in October 2013.
The value is 1.165*10-11. It seems that this value is quite
small. Actually, the absolute value is not important; the relative value matters. If we estimate the
illiquidity for DELL over the same period, we would  nd a value of 0.638*10-11. Since 1.165 is greater
than 0.638, we conclude that IBM is less liquid than DELL.
'''

p = np.array(data.close)
dollar_vol = np.array(data.volume * p)

px = np.array(p[1:])
py = np.array(p[:-1])
ret = (px - py) / px
illiq = np.mean(np.divide(abs(ret), dollar_vol[1:]))

print("Aminud illiq = ", illiq)
########################################################################################################
# Pastor and Stambaugh liquidity measure (2003)
'''
Based on the methodology and empirical evidence in Campbell, Grossman and Wang(1993), Pastor and Stambaugh(2003) designed
the following model to measure individual stock's liquidity and the market liquidity:
'''
rgba1, depth1 = parser.to_rgba(r'$illiq_t = \frac{|R_t|}{P_t*V_t}$', color='black', fontsize=12, dpi=200)
fig = plt.figure()
fig.figimage(rgba1.astype(float) / 255., 100, 100)

plt.show()
plt.clf()

