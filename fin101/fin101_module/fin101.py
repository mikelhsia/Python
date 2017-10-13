import math
def pv_f(fv = 100, r = 0.1, n = 1):
	"""
	:Objective: estimate present value
	:param fv: future value
	:param r: discount periodic rate
	:param n: number of periods
	:return: fv/(1+r)**n
	"""
	pv = fv/(1+r)**n
	return pv


def pv_perpetuity(c = 100, r = 1):
	return c/r


def npv_f(rate, cashflows):
	total = 0
	for i, cashflow in enumerate(cashflows):
		total += cashflow / (1 + rate) ** i

	return total


def  IRR_f(cashflows, interations=100):
	rate = 1.0
	investment = cashflows[0]
	for i in range(1, interations + 1):
		rate *= (1-npv_f(rate, cashflows) / investment)
	return rate


def CND(X):
	'''
	Cumulative standard normal distribution (CND)
	Since a standard normal distribution is symmetric,
	its cumulative distribution will be 0.5 at 0. It is
	also well known that a z value of -2.33 corresponds
	to 1 percent and 1.647 for 95 percent. We could
	use the Excel normdist() function to verify our CND
	function. The structure of the related Excel function
	is normdist(x, mean, standard deviation, cumulative).
	The last one takes 0 for the normal distribution and 1
	for the cumulative distribution as shown in the following
	screenshot:
	:param X:
	:return:
	'''
	(a1, a2, a3, a4 , a5) = (0.31938153, -0.356563782, 1.781477937, -1.821255978, 1.330274429)

	L = abs(X)
	K = 1.0/(1.0 + 0.2316419 * L)
	w = 1.0 - 1.0/math.sqrt(2 * math.pi)*math.exp(-L*L/2.)*(a1*K + a2*math.pow(K, 2) + a3*math.pow(K, 3) + a4 * math.pow(K, 4) + a5 * math.pow(K, 5))

	if X < 0:
		w = 1.0 - w

	return w

## Cumulative standard normal distribution
from scipy.stats import norm as nm

def bs_call(S, X, T, r, sigma):
	"""
	This is black-scholes model to price the European call option
	:param S: Current stock price
	:param X: Exercise price
	:param T: Maturity (in years)
	:param r: continuously compounded risk-free rate
	:param sigma: volatility of the underlying security
	:return: Price of the European call option
	"""
	d1 = (math.log(S/X) + (r + sigma * sigma/2.) * T) / (sigma * math.sqrt(T))
	d2 = d1 - sigma * math.sqrt(T)
	# return S * CND(d1) - X * math.exp(-r * T) * CND(d2)
	return S * nm.cdf(d1) - X * math.exp(-r * T) * nm.cdf(d2)
