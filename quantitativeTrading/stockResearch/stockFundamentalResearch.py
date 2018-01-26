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
import matplotlib.pyplot as plt


def get_funda_finance(security):
    # df = ts.get_balance_sheet('000001') 
    df = ts.get_cash_flow(security) 
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

    dfT.sort_index(ascending=True, inplace=True)

#     print(dfT)
#     print(dfT.columns)
    return df

def main():
    df = get_funda_finance('000625')
    a = df.经营活动现金流入小计.map(lambda x: float(x))
    b = df.经营活动现金流入小计.map(lambda x: 0)

    fig, axes = plt.subplots(1, 1)

    a = a.pct_change()

    p = a[a > 0]
    n = a[a < 0]
    a.plot(kind='bar')
    # a.plot()
    # b.plot()

    # n.plot(kind='bar')
    # p.plot(kind='bar')

if __name__ == '__main__':
    main()
