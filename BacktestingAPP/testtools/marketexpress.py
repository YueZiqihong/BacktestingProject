# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 21:58:49 2020

@author: zymunique
"""
from . import generalsupport as gs
import pandas as pd


class MarketExpress():
    def __init__(self, dbname):
        self.expconn, self.expc = gs.connectDB(dbname)
        self.backDataTable = 'backward_market'
        self.forwardDataTable = 'forward_market'

    def getBackMarketData(self, column_list=None, filter_dict=None):
        """
        获取前复权的数据.
        column_list是SQL语句中的字段名.
        filter_dict则为SQL语句where语句中的限制条件, 是一个dictionary. dictionary
        的key是字段名, value是一个list, 表明限制的条件.
        如果key是trade_date, 则只允许输入两个值, 表明起止日期.
        """
        statement = gs.queryGenerator(self.backDataTable,
                                      column_list,
                                      filter_dict)
        return pd.read_sql_query(statement, self.expconn)

    def getFowardMarketData(self, column_list=None, filter_dict=None):
        """
        请参考getBackMarketData数据, 该函数给出后复权的数据.
        """
        statement = gs.queryGenerator(self.forwardDataTable,
                                      column_list,
                                      filter_dict)
        return pd.read_sql_query(statement, self.expconn)

    def getMarketNow(self, column_list=None, filter_dict=None):
        """
        MarketNow是数据库当中一个由后台自更新的数据表, 只包括current date的股价数据.
        该函数只调用这一天的数据.
        """
        return self.marketnow

    def getTradingCalendar(self, start_date, end_date):
        """
        从MarketExpress数据库中获取部分TradeCalendar并返回日期的List.
        """
        statement = gs.queryGenerator('trade_cal',
                                      None,
                                      {'trade_date': [start_date, end_date]})
        df = pd.read_sql_query(statement, self.expconn)
        return df['trade_date'].tolist()

    def updateMarketNow(self, date, how):
        """
        给定一个日期, MarketNow数据表刷新为当天的数据. 采用how的方式.
        how可以选择forward 或者 backward.
        """
        # 首先根据复权的方式, 决定数据从哪个表格中更新?
        if how == "backward":
            table_name = "backward_market"
        if how == "forward":
            table_name = "forward_market"

        # 生成响应的表格, 注意会首先删除已经存在的marketnow.
        statement = """
        SELECT * FROM {0}
        WHERE trade_date = DATE('{1}');
        """.format(table_name, date)
        self.marketnow = pd.read_sql_query(statement, self.expconn)

    def close(self):
        self.expconn.close()
