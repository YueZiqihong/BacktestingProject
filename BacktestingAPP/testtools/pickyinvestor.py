# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 17:48:13 2020

@author: zymunique
"""

import time
import pandas as pd
import numpy as np
from datetime import datetime
import datamonger

class PickyInvestor():
    def __init__(self):
        self.datamonger = datamonger.Datamonger()
        self.hushen300df = self.datamonger.getHuShen300IndexComponent()
        pass
    
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
        trading_book_info  = {'yz' : {'cash' : 20000000},
                              'jx' : {'cash' : 30000000}}
        return trading_book_info
        
    def myTradingOpen(self):
        
        start = time.time()
        # myRandomSet = ['000830.SZ' , '603288.SH', '601166.SH']
        # if datetime.strptime(self.currentDate, "%Y-%m-%d").weekday() == 0:
        #         self.brokerdb.userSendMarketOrderMany([('yz', '000830.SZ', 1000, 'shares')] * 50)
        #         self.brokerdb.userSendMarketOrderMany([('jx', '603288.SH', 1000, 'shares')] * 50)
            
        # if datetime.strptime(self.currentDate, "%Y-%m-%d").weekday() == 4:
        #         self.brokerdb.userSendMarketOrderMany([('yz', '000830.SZ', -1000, 'shares')] * 50)
        #         self.brokerdb.userSendMarketOrderMany([('jx', '603288.SH', -80000, 'value')] * 50)
        aaa = pd.DataFrame()
        
        aaa['ts_code'] = self.hushen300df['con_code']

        aaa['book'] = ['yz','jx'] * 150
        
        np.random.seed(1)
        aaa['amount'] = np.random.randint(-1000, 1000, size = 300)
        
        aaa['amount_type'] = 'shares'
        
        aaa = aaa.reindex(columns=['book', 'ts_code', 'amount', 'amount_type'])
        
        orders = aaa.to_records(index = False).tolist()
        
        self.brokerdb.userSendMarketOrderMany(orders)

        end = time.time()
        print("Nice Morning.", self.currentDate, print(end-start))
        
        
        
    def myTradingIntra(self):
        pass
    
    def myTradingClose(self):
        pass
    