'''
Chap 5
Bond and Stock Valuation
'''

def APR2Rm(APR1,m1,m2):
	"""
	Objective: convert one APR to another effective rate Rm:
     APR1: annual percentage rate
       m1: compounding frequency for APR1
       m2: effective period rate of our target effective rate
	Formula used: Rm=(1+APR1/m1)**(m1/m2)-1 Example #1>>>APR2Rm(0.1,2,4)
            0.02469507659595993
	"""
	return (1+APR1/m1)**(m1/m2)-1



def APR2APR(APR1,m1,m2):
	return m2*((1+APR1/m1)**(m1/m2)-1)

'''
For a continuously compounded interest rate, different ways could be used to explain this confusion concept. 
First, we apply the formula of Effective Annual Rate (EAR) by increasing the compounding frequency of m:
'''
def EAR_f(APR,m):
	return (1+APR/m)**m-1

'''
Assume that the APR is 10% and let's increase the compounding frequency, see the following program
'''
import numpy as np
d = 365
h = d * 24
m = h * 60
s = m * 60
ms = s * 100
x = np.array([1, 2, 4, 12, d, h ,m, s, ms])

APR = 0.1

for i in x:
	print(EAR_f(APR, i))