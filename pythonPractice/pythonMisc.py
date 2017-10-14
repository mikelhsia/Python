# 變量類型註釋
######################################################################################################
# int and str are simply a comment, doesn't really force the variable to change their types
def add(a: int, b: int) -> str:
	print(a+b)

# 數字字符串特殊操作
######################################################################################################
# 下滑線在數字中並不會影響數字本身，只是在代碼中更好的視覺上分辨數字長度
a = 1_000_000_000
a = 0xEEFE_AF98

# Use f and {} to put variables directly in the string
a = "lai lai ali"
b = f"hello {a}"
print(b)    # hello lai lai lai

# Put math or array in {}
a = f"hello {100*2/3}"
print(a)    # 66.667

a = f"hello {[1] + [2]}"
print(a)    # [1, 2]

# 處理路徑
######################################################################################################
import os
# Old method
print(os.path.join(os.path.join(os.path.dirname(os.path.dirname((os.path.abspath(__file__))), "PythonTools"), "csv2excel.py")))

# New method
import pathlib
config_path = pathlib.Path(__file__).parent.parent / "PythonTools" / "csv2excel.py"
print(config_path.read_text())
print(config_path.stem)
print(config_path.is_dir())
print(config_path.exists())
