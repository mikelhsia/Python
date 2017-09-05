import sys
myFolder = "/Users/tsuyuhsia/Desktop/Python/fin101"

if myFolder not in sys.path:
	sys.path.append(myFolder)

import fin101.fin101 as fn

print(fn.pv_f (100, 0.1, 2))

