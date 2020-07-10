# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 18:29:34 2020

@author: zymun
"""

from . import generalsupport as gs
import pandas as pd

class Datamonger:
    def __init__ (self):
        self._dbname = "testMarket.db"
        self.mktconn, self.mktc = gs.connectDB(self._dbname)
        self.dataconn = gs.connectTS()

    def getRawDailyMarketData(self, start_date, end_date, stock_pool = None, columns = None):
        """
        提供市场未复权数据和复权因子等
        stock_pool: List/Series
        """
        # 首先处理字段名
        columns_str = gs.handleQueryColumnsList(columns)

        # 处理日期
        start_date = gs.addDashtoDate(start_date)
        end_date = gs.addDashtoDate(end_date)

        # 处理stock_pool的数据类型
        stock_list = gs.handleStockPoolType(stock_pool)

        # 如果stock_pool是部分数据
        if stock_list is not None:
            tscode_str = gs.handleQueryStockList(stock_pool)
            statement = """
            SELECT {0}
            FROM marketinfo
            WHERE ts_code IN ({1})
        	AND trade_date BETWEEN DATE ('{2}') AND DATE ('{3}')
            """.format(columns_str, tscode_str, start_date, end_date)

        # 如果是全部的stock_pool, 那么直接转化为
        else:
            statement ="""
            SELECT {0}
            FROM marketinfo
            WHERE trade_date >= date('{1}')
            AND trade_date <= date('{2}')
            """.format(columns_str, start_date, end_date)
        # 返回DataFrame的数据类型
        return pd.read_sql_query(statement, self.mktconn)

    def getValidTradeDate(self, start_date, end_date):
        """
        返回范围内合理的交易日历
        """
        return gs.SQLvalidTradeDate(start_date, end_date, self.mktconn)

    def getHuShen300IndexComponent(self):
        statement = """
        SELECT * FROM Hushen300component
        """
        df = pd.read_sql_query(statement, self.mktconn)
        return df

    def close(self):
        self.mktconn.close()
