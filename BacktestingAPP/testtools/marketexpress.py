# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 21:58:49 2020

@author: zymunique
"""
import generalsupport as gs
import pandas as pd


class MarketExpress():
    def __init__(self, dbname):
        self.expconn, self.expc = gs.connectDB(dbname)
        self.backDataTable = 'backward_market'
        self.forwardDataTable = 'forward_market'
        self.marketNow = 'marketnow'
        
    def getBackMarketData(self, column_list = None, filter_dict = None):
        statement = gs.queryGenerator(self.backDataTable,
                                      column_list,
                                      filter_dict)
        return pd.read_sql_query(statement, self.expconn)
    
    def getFowardMarketData(self, column_list = None, filter_dict = None):
        statement = gs.queryGenerator(self.forwardDataTable,
                                      column_list,
                                      filter_dict)
        return pd.read_sql_query(statement, self.expconn)
        
    def getMarketNow(self, column_list = None, filter_dict = None):
        statement = gs.queryGenerator(self.marketNow,
                                      column_list,
                                      filter_dict)
        return pd.read_sql_query(statement, self.expconn)
        
    def getTradingCalendar(self, start_date, end_date):
        """
        从MarketExpress数据库中获取部分TradeCalendar并返回日期的List.
        """
        statement = gs.queryGenerator('trade_cal',
                                      None,
                                      {'trade_date' : [start_date, end_date]})
        df = pd.read_sql_query(statement, self.expconn)
        return df['trade_date'].tolist()
        
    def updateMarketNow(self, date, how):
        """
        给定一个日期, MarketNow数据表刷新为当天的数据. 采用how的方式.
        how可以选择forward 或者 backward.
        """
        if how == "backward":
            table_name = "backward_market"
        if how == "forward":
            table_name = "forward_market"
        statement = """
        DROP TABLE IF EXISTS marketnow;
        
        CREATE TABLE marketnow AS
        SELECT * FROM {0}
        WHERE trade_date = DATE('{1}');
        """.format(table_name, date)
        self.expc.executescript(statement)
        self.expconn.commit()
        
    def close(self):
        self.expconn.close()
        
