# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 22:50:51 2020

@author: zymun
"""

import generalsupport as gs
import pandas as pd

class Brokerdatabase():
    def __init__(self):
        pass
    
    def createBrokerDatabase(self, dbname):
        """
        为本次回测创建全新做市商数据库记录信息

        Parameters
        ----------
        dbname : String
            准备新建的数据库的名称.

        Returns
        -------
        None.

        """
        self.brokerconn, self.brokerc = gs.createDB(dbname)
    
    def connectBrokerDatabase(self, dbname):
        """
        使用已有的做市商数据库.
        不推荐新完整回测时使用. 
        """
        self.brokerconn, self.brokerc = gs.connectDB(dbname)
        
    def setCurrentDate(self, date):
        """
        给定数据库函数运行的日期, 防止向前更改数据.
        默认输入的date类型是yyyy-mm-dd是由VirtueSE传入的.
        """
        self.current_date = date
        
    def createHistPositionTable(self):
        statement = """
        CREATE TABLE "hist_position" (
        	"book"	TEXT NOT NULL,
        	"ts_code"	TEXT NOT NULL,
            "trade_date" DATE NOT NULL,
        	"position"	NUMERIC,
        	"value"	NUMERIC,
        	"wavg_cost"	NUMERIC,
        	"return"	NUMERIC,
        	"pct_return"	NUMERIC,
    	PRIMARY KEY("book","trade_date","ts_code")
        )
        """
        self.brokerc.execute(statement)
        self.brokerconn.commit()
        
    def createCurrentPositionTable(self):
        statement = """
        CREATE TABLE "current_position" (
        	"book"	TEXT NOT NULL,
        	"ts_code"	TEXT NOT NULL,
        	"position"	NUMERIC,
        	"value"	NUMERIC,
        	"wavg_cost"	NUMERIC,
        	"return"	NUMERIC,
        	"pct_return"	NUMERIC,
        	PRIMARY KEY("book","ts_code")
        )
        """
        self.brokerc.execute(statement)
        self.brokerconn.commit()
        
    def createOrderBookTable(self):
        """
        用于创建在数据库中新建一个order_book表格.

        Returns
        -------
        None.

        """
        statement  = """
        CREATE TABLE "order_book" (
        	"order_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        	"book"	TEXT NOT NULL,
        	"trade_date"	DATE NOT NULL,
        	"ts_code"	TEXT NOT NULL,
        	"order_type"	TEXT NOT NULL,
        	"limit_price"	NUMERIC,
        	"amount"	NUMERIC NOT NULL,
        	"amount_type"	TEXT NOT NULL,
        	"validity_term"	INTEGER,
        	"order_status"	TEXT NOT NULL
        )
        """
        self.brokerc.execute(statement)
        self.brokerconn.commit()
        
    def processOrderBySql(self, book, ts_code, amount, price):
        """
        仅供测试.
        该函数通过Transaction, 使用数据库的操作直接处理订单.
        """
        statement = """
        BEGIN TRANSACTION;

        -- Update Cash
        UPDATE current_position
        SET value = value - 1000 * 400
        WHERE book = 'yz' AND ts_code = 'cash';
        
        -- Update wavg_cost
        UPDATE current_position
        SET wavg_cost = (wavg_cost * position + 1000 * 400) / (position + 1000)
        WHERE book = 'yz' AND ts_code = 'MS';
        
        -- Update Position 
        UPDATE current_position
        SET position = position + 1000
        WHERE book = 'yz' AND ts_code = 'MS';
        
        -- UPDATE value, return and pct_return
        UPDATE current_position
        SET value = position * 400
        WHERE book = 'yz' AND ts_code = 'MS';
        
        UPDATE current_position
        SET return = value - wavg_cost * position
        WHERE book = 'yz' AND ts_code = 'MS';
        
        UPDATE current_position
        SET	pct_return = return/(wavg_cost * position)
        WHERE book = 'yz' AND ts_code = 'MS';
        
        COMMIT;
        """
        self.brokerc.execute(statement)
        self.brokerconn.commit()
        
    def userSendMarketOrderMany(self, order_tuple_list):
        """
        用于用户批量下单, 数据库一次性执行INSERT相关语句.
        传过来的参数应该是:
        [(book, ts_code, amount, amount_type)]
        """
        statement = """
        INSERT INTO order_book
        VALUES (NULL, ?, DATE('{0}'), ?, 'market', NULL, ?, ?, NULL, 'pending')
        """.format(self.current_date)
        
        self.brokerc.executemany(statement, order_tuple_list)
        self.brokerconn.commit()
        
    def userSendMarketOrder(self, book, ts_code, amount):
        """
        由用户调取该函数, 发送一个market order, 然后直接写入数据表格order_book中
        """
        # sample_market_order = {"book" : "yz",
        #                 "trade_date" : "2020-06-01",
        #                 "ts_code" : "MS",
        #                 "order_type" : "market",
        #                 "amount" : 500,
        #                 "amount_type" : "shares"}
        statement = """
        INSERT INTO order_book
        VALUES (
        	NULL,
        	'{0}',
        	DATE ('{1}'),
        	'{2}',
        	"market",
        	NULL,
        	{3},
        	"shares",
        	NULL,
            'pending'
        	) 
        """.format(book, self.current_date, ts_code, amount)
        self.brokerc.execute(statement)
        self.brokerconn.commit()
        
    def userSendMarketOrderByValue(self, book, ts_code, amount):
        """
        由用户调取该函数, 发送一个market order, 然后直接写入数据表格order_book中
        """
        statement = """
        INSERT INTO order_book
        VALUES (
        	NULL,
        	'{0}',
        	DATE ('{1}'),
        	'{2}',
        	"market",
        	NULL,
        	{3},
        	"value",
        	NULL,
            'pending'
        	) 
        """.format(book, self.current_date, ts_code, amount)
        self.brokerc.execute(statement)
        self.brokerconn.commit()
        
    def userSendLimitOrder(self, book, ts_code, price, amount, validity_term = "NULL"):
        """
        由用户生成Limit Order, 由于target price既定, 所以只需要amount_type只需要shares即可.

        Parameters
        ----------
        book : string
            账户名.
        ts_code : string
            股票交易代码.
        price : Number
            Limit Price的价格.
        amount : Number
            交易股票数量.
        validity_term : Number, optional
            该订单的有效期. The default is "NULL".

        Returns
        -------
        直接写入数据库

        """
        
        statement = """
        INSERT INTO order_book
        VALUES (
        	NULL,
        	'{0}',
        	DATE ('{1}'),
        	'{2}',
        	"limit",
        	{3},
        	{4},
        	"shares",
        	{5},
            'pending'
        	)
        """.format(book, self.current_date, ts_code, price, amount, validity_term)
        self.brokerc.execute(statement)
        self.brokerconn.commit()

    def readMarketPendingOrder(self):
        statement = """
        SELECT * FROM order_book 
        WHERE order_status = 'pending'
        AND order_type = 'market'
        """
        return pd.read_sql_query(statement, self.brokerconn)
    
    def readLimitPendingOrder(self):
        statement = """
        SELECT * FROM order_book 
        WHERE order_status = 'pending'
        AND order_type = 'market'
        """
        return pd.read_sql_query(statement, self.brokerconn)
    
    def readCurrentPosition(self, book_list = None, ts_code_list = None):
        filter_dict = {'book' : book_list, 'ts_code' : ts_code_list}
        statement = gs.queryGenerator('current_position', None, filter_dict)
        return pd.read_sql_query(statement, self.brokerconn)
    
    def updateOrderStatus(self, id_status_tuple_list):
        """
        批量修改order_book中的订单状态. 

        Parameters
        ----------
        id_status_tuple_list : List of Tuple
            每一个element中是一个Tuple类型的变量, 第一个值为新的order_status
            第二个值为order_id.

        Returns
        -------
        None.

        """
        statement = """
        UPDATE order_book
        SET order_status  = ?
        WHERE order_id = ?
        """
        self.brokerc.executemany(statement, id_status_tuple_list)
        self.brokerconn.commit()
        
    def updateCurrentPosition(self, userPosition, include_index = True):
        """
        特别注意本函数中会将dataframe的index也放进数据库中. 默认给定的userPosition数据库是有索引的!
        """
        userPosition.to_sql('current_position',
                            self.brokerconn,
                            if_exists = 'replace',
                            index = include_index)
        
    def updateHistPosition(self, userCurrentPosition):
        """
        目的是每天通过userCurrentPosition, 加入日期后, 导入历史持仓中

        Parameters
        ----------
        userCurrentPosition : DataFrame

        Returns
        -------
        None.

        """
        # 将今天的数据的日期列全部设置为当前的日期.
        userCurrentPosition['trade_date'] = self.current_date
        # 使用append模式把数据全部更新即可.
        userCurrentPosition.to_sql('hist_position',
                                   self.brokerconn,
                                   if_exists = 'append',
                                   index = False)
    
    def initialDepositCash(self, book_tuple_list):
        """
        为账户设置初始的资金. 将会把'book'和'cash' INSERT进入current_position中.
        适用于开始回测阶段, 用户给定初始资金等.

        Parameters
        ----------
        book_tuple_list : List of Tuple.
            每一个tuple代表一个账户, 第一参数是账户名, 第二个是现金数量.

        Returns
        -------
        None.

        """
        statement = """
        INSERT INTO current_position 
        (book, ts_code, position, value, wavg_cost, return, pct_return)
        VALUES(?, 'cash', ?, NULL, NULL, NULL, NULL)
        """
        self.brokerc.executemany(statement, book_tuple_list)
        self.brokerconn.commit()
        
    def close(self):
        self.brokerconn.close()
    
