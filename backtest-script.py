# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:27:09 2019

@author: Dominic Yuen
"""

import pandas as pd
import numpy as np
from math import sqrt

#input the variableto backtest (sum: bound = 12, step = 0.1; avg: bound = 0.6, step = 0.01)
score = 'score (avg)'
bound = 0.6
step = 0.01

#dataframe and other variables setup
df = pd.read_excel('sentiment_scores_bt_data.xlsx', 'bt', index_col = 0, parse_dates = True)
df = df.fillna(method = 'ffill').dropna()
df['p_%chg'] = df['close'].pct_change()
res = []

#input transaction costs
tc = 10/(8500*5)

#optimizer
for i in np.arange(0, bound, step):
    try:
        df['posi'] = np.where(df[score]>i, 1, np.where(df[score]<-i, -1, 0))
        df['pnl'] = df['posi'].shift(1) * df['p_%chg'] - abs(df['posi'].diff()) * tc
        sr_is = df['pnl'].iloc[:371].mean() / df['pnl'].iloc[:371].std() * sqrt(252)
        sr_os = df['pnl'].iloc[371:].mean() / df['pnl'].iloc[371:].std() * sqrt(252)
        res.append([sr_is, sr_os, i])   
        
    except:
        res.append(['math error', 'math error', i])
        
opt = pd.DataFrame(res)
opt.columns = ['sr_is', 'sr_os', 'thres']
opt = opt[opt['sr_is'] != 'math error'].sort_values(by = 'sr_is', ascending = False)
print(opt.head())        

#optimized result plotting 
thres = opt['thres'].iloc[0]
df['posi'] = np.where(df[score]>thres, 1, np.where(df[score]<-thres, -1, 0))
df['pnl'] = df['posi'].shift(1) * df['p_%chg'] - abs(df['posi'].diff()) * tc
df['cpnl'] = df['pnl'].cumsum()
df['cpnl'].plot()
