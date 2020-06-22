# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 22:15:52 2020

@author: zymunique
"""

"""
测试 monobroker.py
"""

# 初始化一个brokerdatabase 实例
import monobroker
import brokerdatabase
import marketexpress

# 初始化一个brokerdatabase 实例, 该实例链接一个已有的数据库
brokerdb = brokerdatabase.Brokerdatabase()
brokerdb.connectBrokerDatabase("testBroker.db")
brokerdb.setCurrentDate('2020-06-01')

# 初始化一个marketexpress实例
marketdb  = marketexpress.MarketExpress("tempData.db")

# 再初始化一个monobroker实例, 该实例加载一个brokerdatabase对象.
monobroker = monobroker.MonoBroker()
monobroker.setBrokerDatabase(brokerdb)
monobroker.setMarketDatabase(marketdb)
##### 测试你喜欢的东西吧

"""
测试 virtuese.py
"""
import virtuese as vs
import pickyinvestor
import datamonger

dp = datamonger.Datamonger()
df2 = dp.getHuShen300IndexComponent()


# 初始化一个对象实例
backtrader = vs.VirtueSE()

# 必须设置回测日期
backtrader.setRunningInterval('20190601', '20200601')

# 必须设置价格回测方式
backtrader.setBacktestingPriceEngine("backward")

# 可选设置一个股票池
backtrader.setStockPool(df2['con_code'].tolist())

# 可选创建本次回测的临时数据库
# backtrader.createMarketExpressDB("testMarket.db", "20200613DTestME.db")
# 加载两个数据库
backtrader.setBrokerDB("aTest.db")
backtrader.setMarketExpressDB("20200613DTestME.db")

# 初始化策略实例
strategy = pickyinvestor.PickyInvestor()

# 加载策略
backtrader.setTradingStrategy(strategy)

backtrader.execute()

######################################################################
import pandas as pd
import numpy as np
import datamonger
import time

np.random.rand()

stock_code = datamonger.Datamonger().getRawDailyMarketData('20200601', '20200601', None, ['ts_code'])

def letstry(df, values):
    print('我开始了')
    print(values)
    df.loc['000001.SZ', 'number'] = 0.23
    if values > 2000:
        result =  "you are a good man", df
    else:
        result =  "you are a bad man", df
    return result
    

    
test_df = pd.DataFrame()

test_df['ts_code'] = stock_code['ts_code']
test_df['number1'] = np.arange(3812)
test_df['number2'] = np.arange(3812)
test_df.set_index('ts_code', inplace = True)

empty_set = []

start = time.time()
for i in range(10):
    for index, row in test_df.iterrows():
        message, test_df = letstry(test_df)
        empty_set.append(message)
end = time.time()
print(end - start)

test_df['trash'], test_df = divide(test_df, test_df['number1'].values)


def divide(a, b):
    if b == 0:
        return 0.0
    return float(a)/b


test_df['result'] = np.vectorize(divide)(test_df['number1'], test_df['number2'])

######################
test_dfa = pd.DataFrame()
test_dfa['ts_code'] = stock_code['ts_code']
test_df['number'] = np.arange(3812)

import generalsupport as gs
ttt = np.random.randint(-100000, 100000, size = 6000000)
slow_total = np.vectorize(gs.calculateCommission)(ttt)

ttt_tobroker = np.maximum(np.abs(ttt) * 0.00012, np.full_like(ttt, 5))
ttt_tax = np.abs(np.minimum(ttt * 0.001, np.full_like(ttt, 0)))
ttt_total = ttt_tobroker + ttt_tax

np.sum(slow_total - ttt_total)



test_df = pd.DataFrame()
test_df['name'] = ['yz', 'jx'] * 5
test_df['money'] = np.arange(10)
test_df.groupby('name').cumsum()

###############################################
"""
测试brokerdatabase
"""

