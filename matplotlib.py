#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

# import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(1, 2*np.pi, 50)
plt.plot(x, np.sin(x), x, np.cos(x), x, np.tan(x))
plt.show()

# x = np.random.randn(1000)
# plt.hist(x, 50)
# plt.show()

a = np.arange(5)
print a.dtype
print a
print a.shape 

