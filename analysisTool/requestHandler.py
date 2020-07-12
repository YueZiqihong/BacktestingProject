from .testtools import virtuese as vs
from .testtools import pickyinvestor
import datetime
import numpy as np
import pandas as pd
import os

from .models import TradeCalendar
from .models import Position

def getDateIDs():
    tradeID = {}
    tradeDays = TradeCalendar.objects.all()
    for tradeDay in tradeDays:
        tradeID[tradeDay.trade_date.strftime("%Y-%m-%d")] = tradeDay.id
    return tradeID

def getIndex(information):
    """
    Adjust order so that indexes is a list such that:
    indexes[] are the index for information to be storaged correctly.
    information[indexes[0]] - book
    information[indexes[1]] - ts_code
    information[indexes[2]] - trade_date
    information[indexes[3]] - position
    information[indexes[4]] - value
    information[indexes[5]] - wavg_cost
    information[indexes[6]] - return
    information[indexes[7]] - pct_return
    """
    indexes = []
    indexes.append(information.index("book"))
    indexes.append(information.index("ts_code"))
    indexes.append(information.index("trade_date"))
    indexes.append(information.index("position"))
    indexes.append(information.index("value"))
    indexes.append(information.index("wavg_cost"))
    indexes.append(information.index("return"))
    indexes.append(information.index("pct_return"))
    return indexes

def simulate(params):
    response = {}
    try:
        startDate = params['startDate']
        endDate = params['endDate']
        stockPool = params['stockPool']
        strategy = params['strategy']
        testval = [startDate,endDate,stockPool,strategy]
        
        # 自己测的时候可以手动输入
        startDate = '20200301'
        endDate = '20200603'
        stockPool = [] # 之后我处理，应该是一个列表，每一项是一个ticker
        strategy = "" # 可以先自己写


        backtest = vs.VirtualSE()
        # 设置回测日期
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

        transactionDataFile = backtest.getTransactionData()
        tradeID = getDateIDs()
        skipFirstLine = True
        for line in transactionDataFile:
            if skipFirstLine:
                skipFirstLine = False
                indexes = getIndex(line.split()[0].split(","))
                Position.objects.all().delete()
                statements = []
                continue

            infomation = line.split()[0].split(",")

            value = infomation[indexes[4]] if infomation[indexes[4]]!="" else 0
            return_field = infomation[indexes[6]] if infomation[indexes[6]]!="" else 0
            pct_return = infomation[indexes[7]] if infomation[indexes[7]]!="" else 0

            statements.append(Position(
            book=infomation[indexes[0]],
            ts_code=infomation[indexes[1]],
            trade_day_id=tradeID[infomation[indexes[2]]],
            position=infomation[indexes[3]],
            value=value,
            wavg_cost=infomation[indexes[5]],
            return_field=return_field,
            pct_return=pct_return,
            ))
        Position.objects.bulk_create(statements)



        transactionDataFile.close()
        backtest.clear()
        return testval


    except Exception as e:
        print(str(e))


# if __name__ == '__main__':
#     print("f y")
#     generate(0)
