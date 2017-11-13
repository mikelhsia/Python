"""
Description: Practice of Python for Finance 2nd edition 2017
Date: 2017-11-05
Author: Michael Hsia
"""

import scipy as sp

sp.pv(0.024, 3, 0.08*100, 100)
# -116.02473258972169

sp.rate(5, 0.03*1000, -818, 1000)
# YTM = 0.074981804314870726

p0 = sp.pv(0.04, 15, 0, -100)
p1 = sp.pv(0.05, 15, 0, -100)
p = (p1-p0) /p0
# p0 55.526450271327484
# p1 48.101709809096995

p0 = sp.pv(0.04, 30, -0.09*100, -100)
p1 = sp.pv(0.05, 30, -0.09*100, -100)
p = (p1-p0) /p0
# p0 186.46016650332245
# p1 161.48980410753134
# Based on the preceding results, the 30-year coupon bond is riskier than the 15- year zero coupon bond since it has a bigger percentage change
