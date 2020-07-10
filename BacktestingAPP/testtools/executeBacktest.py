# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:35:38 2020

@author: zymunique
"""

from . import virtuese as vs
from . import pickyinvestor

# 初始化一个对象实例
backtrader = vs.VirtualSE()

# 必须设置回测日期
backtrader.setRunningInterval('20190601', '20190901')

# 必须设置价格回测方式
backtrader.setBacktestingPriceEngine("backward")

# 可选设置一个股票池
# backtrader.setStockPool(df2['con_code'].tolist())

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
