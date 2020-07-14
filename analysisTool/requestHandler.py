from .testtools import virtuese as vs
from .testtools import pickyinvestor
import datetime
import numpy as np
import pandas as pd
import os

from .models import TradeCalendar
from .models import Position

def getDateIDs():
    """Get a dictionary mapping date to id in the database.
    """
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


        # startDate = '20200301'
        # endDate = '20200603'
        # stockPool = []
        # strategy = ""


        backtest = vs.VirtualSE()
        backtest.setRunningInterval(startDate, endDate)
        backtest.setBacktestingPriceEngine("backward")
        # backtest.setStockPool(stockPool)
        backtest.setBrokerDB("aTest.db")
        backtest.setMarketExpressDB("externalDB.DB")

        strategy = pickyinvestor.PickyInvestor()
        backtest.setTradingStrategy(strategy)
        backtest.execute()

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
