
# 本函数运行只依赖一个框架和一个策略
from . import virtuese as vs
from . import pickyinvestor
import datetime
import numpy as np
import pandas as pd
# virtuese的运行依赖的包已经在virtuese开始声明.
# pickyinvester以来的包也已经声明
# 其余子文件使用的都是基础包, 以及generalsupport这一个个人包


def generate(request):
    response = {}
    try:
        # startDate = datetime.datetime.strptime(request.GET.get("startDate"), '%Y-%m-%d').date()
        # endDate = datetime.datetime.strptime(request.GET.get("endDate"), '%Y-%m-%d').date()
        startDate = '20200301'
        endDate = '20200603'
        strategy = "" # 可以先自己写
        stockPool = [] # 之后我处理，应该是一个列表，每一项是一个ticker
        # 利用上面几个参数 做坏事
        backtest = vs.VirtualSE()
        # 设置回测日期
#        startDate = datetime.datetime.strftime(startDate, '%Y%m%d')
#        endDate = datetime.datetime.strftime(endDate, '%Y%m%d')
        backtest.setRunningInterval(startDate, endDate)
        # 设置价格回测方式
        backtest.setBacktestingPriceEngine("backward")
        # 设置股票池
        # backtest.setStockPool(stockPool)
        # 可选创建本次回测的临时数据库
        # backtest.createMarketExpressDB("testMarket.db", "...")
        ## 加载两个数据库
        backtest.setBrokerDB("aTest.db")
        backtest.setMarketExpressDB("20200613DTestME.db")

        # 初始化策略实例
        strategy = pickyinvestor.PickyInvestor()
        # 加载策略
        backtest.setTradingStrategy(strategy)
        # 运行之后, 可能会报divide的warning无视; 产生log文件无视; 生成csv文件默认不包括表头(由于多次写入)
        # book,ts_code,position,value,wavg_cost,return,pct_return
        backtest.execute()

        # 标注一下即可，最后我需要处理数据类型才能正常连

    except Exception as e:
        print(str(e))


# if __name__ == '__main__':
#     print("f y")
#     generate(0)
