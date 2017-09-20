import sys
import chardet
import pandas as pd
import numpy as np

# if (__name__ == '__main__') and sys.argv[0] and sys.argv[1]:
if (__name__ == '__main__'):

	fin = sys.argv[1]
	print(fin)
	print(type(fin))
	fout = sys.argv[2]
	print(fout)
	print(type(fout))

	# with open('/Users/tsuyuhsia/Desktop/PiwikExport.csv', 'rb') as f:
	with open(fin, 'rb') as f:
		result = chardet.detect(f.read())  # or readline if the file is large

	df=pd.read_csv(fin, header=None, error_bad_lines=False, encoding=result['encoding'])
	print("Encoding method: ", result['encoding'])
	print(df.head())
	# print(df.tail())o

	writer = pd.ExcelWriter('/Users/tsuyuhsia/Desktop/output.xlsx')
	writer = pd.ExcelWriter(fout)
	df.to_excel(writer,'Sheet1')
	writer.save()
