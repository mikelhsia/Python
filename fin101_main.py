import sys

def print_breakline():
	print("---------------------")

myFolder = "/Users/tsuyuhsia/Desktop/Python/fin101"

if myFolder not in sys.path:
	sys.path.append(myFolder)

import fin101.fin101 as fn

print(fn.pv_f (100, 0.1, 2))
print_breakline()

import numpy as np

x = np.array([[1,2,3],
              [3,4,6]])

# Number of data items
print(np.size(x))
# Number of columns
print(np.size(x[1]))
# Standard deviation
print(np.std(x))
# Standard deviation of the first row
print(np.std(x,1))

# Pay attention to the format
total = x.sum()
# 50 random obs from [0.0, 1]
z = np.random.rand(50)
print(z)
# from standard normal
y = np.random.normal(size=100)
print(y)
# from 0, 0.01, ..., 0.99
r = np.array(range(0, 100), float)/100
print(r)

print_breakline()


# dtype is the keyword specifying the data type.
x1=[1,2,3,20]
print(np.array(x1,dtype=float))


print_breakline()
import scipy as sp

cashflows = [50, 40, 20, 10, 50]
# The np.npv() function estimates the present values for a given set of future cashflows.
npv = sp.npv(0.1, cashflows)
print("NPV = ", round(npv, 2))


# The sp.pmt() function is used to answer the following question:
# What is the monthly cash  ow to pay off a mortgage of $250,000
# over 30 years with an annual percentage rate (APR) of 4.5 percent,
# compounded monthly?

payment = sp.pmt(0.045/12, 30*12, 250000)
print("APR = ", round(payment, 2))

# Here, Π xi = x1 ∗ x2 ∗...∗ xn . Assume that we have three numbers a, b, and c. Then
# n i=1 # their arithmetic mean is (a+b+c)/3, while their geometric mean is (a*b*c)^(1/3).

# Performing array manipulations
pv = np.array([[100, 10, 20.2], [34, 22, 41]])
print("--\n", pv)
x = pv.flatten()
print("--\n", x)
pv2 = np.reshape(x, [3, 2])
print("--\n", pv2, end="\n--------------------------")

print_breakline()

## Cumulative standard normal distribution
from scipy.stats import norm as nm
print(nm.cdf(0))

print("BS European call price = ", round(fn.bs_call(40, 40, 1, 0.03, 0.2), 2))

print_breakline()


# The two commands pick up 20 stocks randomly from 500 available stocks.
# s = np.random.standard_t(10, size=1000)  # from standard-T,df=10
# x = np.random.uniform(low=0.0, high=1.0, size=100)  # uniform
stocks = np.random.random_integers(1, 500, 20)
print(stocks)

print_breakline()
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

x = np.linspace(0, 10, 10)
y = np.exp(-x/3.0)
f = interp1d(x, y)
f2 = interp1d(x, y, kind="cubic")
xnew = np.linspace(0, 10, 40)
plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
# plt.show() if input("Want to show diagram?") == 'y' else print("123")
if input("Want to show diagram?") == 'y' : plt.show()


# Solving linear equations using SciPy
# x+2y+5z = 10
# 2x+5y+z = 8
# 2x+3y+8z = 5

A = sp.mat('[1 2 5; 2 5 1; 2 3 8]')
b = sp.mat('[10; 8; 5]')
# Two different ways ot solving equation
print("Solution 1: \n {}".format(A.I * b))
print("Solution 2: \n {}".format(np.linalg.solve(A, b)))
print_breakline()

# In finance, many issues depend on optimization, such as choosing an optimal
# portfolio with an objective function and with a set of constraints.
# For those cases, we could use a SciPy optimization module called scipy.optimize.
# Assume that we want to estimate the x value that minimizes the value of y,
# where y =3 + x2. Obviously, the minimum value of y is achieved when x
# takes a value of 0.
##############################
# import scipy.optimize as optimize
# print(optimize.fmin(fn.bs_call, 3, (40, 1, 0.03, 0.2)))


# CAPM Capital Assets Pricing Model
#   Ri−Rf =a+βi(Rmkt−Rf)
# Here Ri is the stock i's return; βi is the slope (market risk);
# Rmkt is the market return and Rf is the risk-free rate.
# Eventually, the preceding equation could be rewritten as follows:
#   y=α+β∗x

from scipy import stats
stock_ret = [0.065, 0.0265, -0.0593, -0.001, 0.0346]
mkt_ret = [0.055, -0.09, -0.041, 0.045, 0.022]
beta, alpha, r_value, p_value, std_err = stats.linregress(stock_ret, mkt_ret)

print("Beta: %f, alpha: %f" % (beta, alpha))
print("R-squared: {}".format(r_value ** 2))
print("p-value: {}".format(p_value))
print_breakline()

# Clean up the current plot
plt.clf()

plt.plot([1, 2, 3, 10])
plt.xlabel("x- axis")
plt.ylabel("My numbers")
plt.title("My Fiture")
plt.show()

plt.clf()
