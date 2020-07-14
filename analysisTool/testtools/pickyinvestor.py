import pandas as pd
import numpy as np
from . import datamonger


class PickyInvestor():
    def __init__(self):
        self.hushen300df = ['600038.SH','600522.SH','600406.SH','601800.SH']

    def setBrokerDatabase(self, db_instance):
        self.brokerdb = db_instance

    def setMarketDatabase(self, db_instance):
        self.marketdb = db_instance

    def setCurrentDate(self, date):
        self.currentDate = date

    def myTradingBooks(self):
        """
        Initialize books before backtesting.
        Return:
            trading_book_info: Dictionary
                Key: book name,
                Value: {'cash': NumOfThisAccount}.
        """
        trading_book_info = {'yz': {'cash': 20000000},
                             'jx': {'cash': 30000000}}
        return trading_book_info

    def myTradingOpen(self):
        "Actions before market open. This is a testing demo that send orders randomly."
        tradingDF = pd.DataFrame()
        tradingDF['ts_code'] = self.hushen300df
        tradingDF['book'] = ['yz', 'jx'] * 2
        np.random.seed(1)
        tradingDF['amount'] = np.random.randint(-1000, 1000, size=4)
        tradingDF['amount_type'] = 'shares'
        tradingDF = tradingDF.reindex(columns=['book', 'ts_code', 'amount', 'amount_type'])
        orders = tradingDF.to_records(index=False).tolist()
        self.brokerdb.userSendMarketOrderMany(orders)

    def myTradingIntra(self):
        pass

    def myTradingClose(self):
        pass
