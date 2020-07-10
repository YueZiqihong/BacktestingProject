# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 17:48:13 2020

@author: zymunique
"""

import pandas as pd
import numpy as np
from . import datamonger


class PickyInvestor():
    def __init__(self):
        self.datamonger = datamonger.Datamonger()
        self.hushen300df = ['600038.SH','600522.SH','600406.SH','601800.SH']
#        self.hushen300df = self.datamonger.getHuShen300IndexComponent()

    def setBrokerDatabase(self, db_instance):
        self.brokerdb = db_instance

    def setMarketDatabase(self, db_instance):
        self.marketdb = db_instance

    def setCurrentDate(self, date):
        self.currentDate = date

    def myTradingBooks(self):
        """
        用来传递本次回测时, 需要在broker处初始化的账户信息.

        Returns
        -------
        trading_book_info : Dictionary
            每一个账户名称作为Key, Value是另一个字典包括具体的ts_code.
            现金的ts_code为cash.

        """
        trading_book_info = {'yz': {'cash': 20000000},
                             'jx': {'cash': 30000000}}
        return trading_book_info

    def myTradingOpen(self):
        # 创建空白的dataframe
        aaa = pd.DataFrame()
        # 设置买卖标的
        aaa['ts_code'] = self.hushen300df
        # 设置买卖账户
        aaa['book'] = ['yz', 'jx'] * 2
        # 设置随机数
        np.random.seed(1)
        aaa['amount'] = np.random.randint(-1000, 1000, size=4)
        # 设置买卖类型
        aaa['amount_type'] = 'shares'

        aaa = aaa.reindex(columns=['book', 'ts_code', 'amount', 'amount_type'])

        orders = aaa.to_records(index=False).tolist()

        self.brokerdb.userSendMarketOrderMany(orders)

    def myTradingIntra(self):
        pass

    def myTradingClose(self):
        pass
