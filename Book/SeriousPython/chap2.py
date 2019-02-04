# import itertools
# Equals to
# itertools = __import__("itertools")

# import itertools as it
# Equals to
# it = __import__("itertools")

import sys
import os
print(sys.modules['os'])
print(sys.modules.keys())
print(sys.builtin_module_names)

# It’s important to note that the list will be iterated over to find the requested module
# , so the order of the paths in sys.path is important. It’s useful to put the path most likely to contain the modules
# you are importing early in the list to speed up search time.


