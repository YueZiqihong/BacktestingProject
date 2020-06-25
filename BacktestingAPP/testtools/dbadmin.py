# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 19:56:30 2020

@author: zymun
"""

import sqlite3
import pandas as pd
import generalsupport as gs
import time

class DBadmin:
    def __init__ (self, dbname):
        self.mktconn, self.mktc = gs.connectDB(dbname)
        self.dataconn = gs.connectTS()
    
    def updateDailyPrice(self, trade_date):
        """
        更新一天的未复权行情数据以及当天的复权因子到数据库的marketinfo数据表中
        """
        # 获取当天的日交易数据df
        daily_price = gs.TSdailyAllPrice(self.dataconn, trade_date)
        # 获取当天的因子数据
        daily_factor = gs.TSdailyAllFactor(self.dataconn, trade_date)
        # 合并两个表格
        daily_price = pd.merge(daily_price,
                               daily_factor,
                               on = ['ts_code','trade_date'],
                               how = 'left')
        # 重命名df并只获取相关字段
        daily_price = daily_price[["ts_code",
                            "trade_date",
                            "open",
                            "high",
                            "low",
                            "close",
                            "vol",
                            "pct_chg",
                            "adj_factor"]]
        # 更改date的string格式
        daily_price = gs.convertDatetime(daily_price, "trade_date")
        # 输入database
        daily_price.to_sql('marketinfo', self.mktconn, if_exists='append', index = False)
        return 1
    
    def deleteTableRows(self, tbname):
        gs.SQLdeleteRows(tbname, self.mktconn, self.mktc)
    
    def getTradeCalendar(self, start_date, end_date):
        return gs.SQLvalidTradeDate(start_date, end_date, self.mktconn)
    
    def updateMultipleDatePrice(self, start_date, end_date):
        """
        从trade_cal表格中返回合理的交易日期并根据该日期运行updateDailyPrice函数更新每一天的行情数据
        """
        trade_cal = self.getTradeCalendar(start_date, end_date)
        for eachdate in trade_cal:
            start_time = time.process_time()
            try:
                self.updateDailyPrice(gs.removeDashFromDate(eachdate))
                print("Update Marketinfo on {0}".format(eachdate))
            except sqlite3.IntegrityError:
                print("Insert values Failed. {0} data probably exists.")
            time.sleep(1)
            end_time = time.process_time()
            print("time:{0}".format(end_time - start_time))
    
    def updateLatestFactorTable(self, trade_date):
        """
        用于更新最新因子数据的表格latest_factor
        由于采用的replace的模式, 因此会覆盖原有数据, 相当于重新创建
        """
        daily_factor = gs.TSdailyAllFactor(self.dataconn, trade_date)
        daily_factor = gs.convertDatetime(daily_factor, "trade_date")
        daily_factor.to_sql('latest_factor', self.mktconn, if_exists = 'replace', index=False)
        
    def createBackwardPriceTable(self):
        """
        创建前复权数据库, 依赖latest factor和marketinfo两个表中的数据
        """
        return None
    def updateBackwardPriceTable(self):
        """
        更新前复权数据库, 由于前复权数据会随着latest factor的刷新而刷新, 因此需要在更新之前, 先删去, 再添加.
        """
        return None
    
    def updateHuShen300IndexComponent(self):
        """
        更新沪深300本月初的成分股
        """
        this_month_start_str = gs.thisMonthStart()
        df = self.dataconn.index_weight(index_code='399300.SZ', start_date = this_month_start_str)
        df.rename(columns={'con_code' : 'ts_code'})
        df.to_sql('Hushen300component', self.mktconn, if_exists = 'replace', index = False)
        
    def updateTradeCalendar(self):
        """
        增量更新trade_cal表格中的数据;
        """
        # 获取当前trade_cal中的最新日期
        
        # 获取当前的日期
        
        # 将两个日期的参数传入API, 获得df
        
        # 将df写入trade_cal中, 方式为append
    
    
    
    def closeConnection(self):
        self.mktconn.close()
        


import generalsupport as gs
from datetime import datetime


# 获取指数列表.

df = tushare_bar.index_daily(ts_code='399300.SZ', start_date='', end_date='20200613')

df2 = tushare_bar.index_weight(index_code='399300.SZ', start_date = this_month_start_str)


myadmin = DBadmin("testMarket.db")
myadmin.updateHuShen300IndexComponent()
