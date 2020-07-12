# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 22:50:51 2020

@author: zymun
"""

from . import generalsupport as gs
import pandas as pd


class Brokerdatabase():
    def __init__(self):
        self.flag = True
        pass

    def createBrokerDatabase(self, dbname):
        """
        为本次回测创建全新做市商数据库记录信息
        """
        self.brokerconn, self.brokerc = gs.connectDB(dbname)

    def connectBrokerDatabase(self, dbname):
        """
        使用已有的做市商数据库.
        不推荐新完整回测时使用.
        """
        self.brokerconn, self.brokerc = gs.connectDB(dbname)

    def setCurrentDate(self, date):
        """
        更新当前的日期
        默认输入的date类型是yyyy-mm-dd是由VirtualSE传入的.
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
        # statement = """
        # CREATE TABLE "current_position" (
        # 	"book"	TEXT NOT NULL,
        # 	"ts_code"	TEXT NOT NULL,
        # 	"position"	NUMERIC,
        # 	"value"	NUMERIC,
        # 	"wavg_cost"	NUMERIC,
        # 	"return"	NUMERIC,
        # 	"pct_return"	NUMERIC,
        # 	PRIMARY KEY("book","ts_code")
        # )
        # """
        # self.brokerc.execute(statement)
        # self.brokerconn.commit()
        # 将current position作为一个属性, 并且默认设定多重索引.
        self.currentPosition = pd.DataFrame([], columns=[
                                            'book', 'ts_code', 'position', 'value', 'wavg_cost', 'return', 'pct_return'])
        self.currentPosition.set_index(['book', 'ts_code'], inplace=True)

    def createOrderBookTable(self):
        """
        用于创建在数据库中新建一个order_book表格.
        """
        statement = """
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

    # def userSendMarketOrder(self, book, ts_code, amount):
    #     """
    #     由用户调取该函数, 发送一个market order, 然后直接写入数据表格order_book中
    #     """
    #     # sample_market_order = {"book" : "yz",
    #     #                 "trade_date" : "2020-06-01",
    #     #                 "ts_code" : "MS",
    #     #                 "order_type" : "market",
    #     #                 "amount" : 500,
    #     #                 "amount_type" : "shares"}
    #     statement = """
    #     INSERT INTO order_book
    #     VALUES (
    #     	NULL,
    #     	'{0}',
    #     	DATE ('{1}'),
    #     	'{2}',
    #     	"market",
    #     	NULL,
    #     	{3},
    #     	"shares",
    #     	NULL,
    #         'pending'
    #     	)
    #     """.format(book, self.current_date, ts_code, amount)
    #     self.brokerc.execute(statement)
    #     self.brokerconn.commit()

    # def userSendMarketOrderByValue(self, book, ts_code, amount):
    #     """
    #     由用户调取该函数, 发送一个market order, 然后直接写入数据表格order_book中
    #     """
    #     statement = """
    #     INSERT INTO order_book
    #     VALUES (
    #     	NULL,
    #     	'{0}',
    #     	DATE ('{1}'),
    #     	'{2}',
    #     	"market",
    #     	NULL,
    #     	{3},
    #     	"value",
    #     	NULL,
    #         'pending'
    #     	)
    #     """.format(book, self.current_date, ts_code, amount)
    #     self.brokerc.execute(statement)
    #     self.brokerconn.commit()

    def userSendLimitOrder(self, book, ts_code, price, amount, validity_term="NULL"):
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

    def readCurrentPosition(self, book_list=None, ts_code_list=None):
        # filter_dict = {'book': book_list, 'ts_code': ts_code_list}
        # statement = gs.queryGenerator('current_position', None, filter_dict)
        # return pd.read_sql_query(statement, self.brokerconn)
        idx = pd.IndexSlice
        # 如果没有任何的限制条件, 那么返回整个当前的仓位dataframe
        if book_list is None and ts_code_list is None:
            return self.currentPosition
        # 如果只对ts_code_list有限制, 那么
        elif book_list is None:
            return self.currentPosition.loc[idx[:, ts_code_list], :]
        # 如果只对book_list有限制, 那么
        elif ts_code_list is None:
            return self.currentPosition.loc[idx[book_list, :], :]
        # 如果对两个条件都有限制.
        else:
            return self.currentPosition.loc[idx[book_list, ts_code_list], :]

    def updateOrderStatus(self, id_status_tuple_list):
        """
        批量修改order_book中的订单状态.

        Parameters
        ----------
        id_status_tuple_list : List of Tuple
            每一个element中是一个Tuple类型的变量, 第一个值为新的order_status
            第二个值为order_id.
        """
        statement = """
        UPDATE order_book
        SET order_status  = ?
        WHERE order_id = ?
        """
        self.brokerc.executemany(statement, id_status_tuple_list)
        self.brokerconn.commit()

    def updateCurrentPosition(self, userPosition, include_index=True):
        """
        默认current position这个dataframe是要包含索引的!
        """
        if include_index:
            self.currentPosition = userPosition
        else:
            self.currentPosition = userPosition.set_index(['book', 'ts_code'])

    def updateHistPosition(self, userCurrentPosition):
        """
        默认传入的userCurrentPosition是包括双重索引的, 因此to_sql时候的index为True
        """
        # 将今天的数据的日期列全部设置为当前的日期.
        userCurrentPosition['trade_date'] = self.current_date
        # 使用append模式把数据全部更新即可.
        userCurrentPosition.to_sql('hist_position',
                                   self.brokerconn,
                                   if_exists='append',
                                   index=True,
                                    header = False)

    def updateHistPositionCSV(self, userPosition):
        """
        使用csv文件储存每天的仓位.
        """
        userPosition['trade_date'] = self.current_date
        if self.flag:
            userPosition.to_csv('hist_position.csv', index=True, mode = 'a', header = True)
            self.flag = False
        else:
            userPosition.to_csv('hist_position.csv', index=True, mode='a', header=False)

    def initialDepositCash(self, book_initial_dict):
        """

        """
        # statement = """
        # INSERT INTO current_position
        # (book, ts_code, position, value, wavg_cost, return, pct_return)
        # VALUES(?, 'cash', ?, NULL, NULL, NULL, NULL)
        # """
        # self.brokerc.executemany(statement, book_tuple_list)
        # self.brokerconn.commit()
        for eachname in book_initial_dict:
            # 生成一个双重索引
            idx = pd.MultiIndex.from_product([[eachname], ['cash']], names=['book', 'ts_code'])
            # 把Cash的值附进去
            df = pd.DataFrame([[book_initial_dict[eachname]['cash']]], index = idx, columns=['position'])
            # concat到已有的position表格中, 也就相当于设定了初始资金.
            self.currentPosition = pd.concat([self.currentPosition,df])

    def close(self):
        self.brokerconn.close()
