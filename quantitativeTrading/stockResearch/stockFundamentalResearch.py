"""
Strategy name: 
Date: 2018/01/26
Author: Michael Hsia
Description: 
"""
import tushare as ts
import numpy as np
import pandas as pd
import datetime


def main():
    df = ts.get_balance_sheet('600518') 
    list = df.报表日期.tolist()
    
    list.reverse()
    list.append('报表日期')
    list.reverse()

    dfT = df.T
    dfT.reset_index(inplace=True)

    list2 = dfT.columns.tolist()
    dic = dict(zip(list2, list)) 

    dfT.rename(columns=dic, inplace=True)
    dfT.drop(0, inplace=True)  

    dfT.报表日期 = dfT.报表日期.map(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
    dfT.set_index(dfT.报表日期, inplace=True)  
    dfT.drop('报表日期', axis=1, inplace=True)   

    print(dfT)

if __name__ == '__main__':
    main()
