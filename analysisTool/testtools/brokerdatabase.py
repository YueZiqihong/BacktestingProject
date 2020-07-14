from . import generalsupport as gs
import pandas as pd

class Brokerdatabase():
    def __init__(self):
        self.flag = True
        pass

    def createBrokerDatabase(self, dbname):
        self.brokerconn, self.brokerc = gs.connectDB(dbname)

    def connectBrokerDatabase(self, dbname):
        self.brokerconn, self.brokerc = gs.connectDB(dbname)

    def setCurrentDate(self, date):
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
        self.currentPosition = pd.DataFrame([], columns=[
                                            'book', 'ts_code', 'position', 'value', 'wavg_cost', 'return', 'pct_return'])
        self.currentPosition.set_index(['book', 'ts_code'], inplace=True)

    def createOrderBookTable(self):
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
        statement = """
        INSERT INTO order_book
        VALUES (NULL, ?, DATE('{0}'), ?, 'market', NULL, ?, ?, NULL, 'pending')
        """.format(self.current_date)

        self.brokerc.executemany(statement, order_tuple_list)
        self.brokerconn.commit()


    def userSendLimitOrder(self, book, ts_code, price, amount, validity_term="NULL"):
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
        idx = pd.IndexSlice
        if book_list is None and ts_code_list is None:
            return self.currentPosition
        elif book_list is None:
            return self.currentPosition.loc[idx[:, ts_code_list], :]
        elif ts_code_list is None:
            return self.currentPosition.loc[idx[book_list, :], :]
        else:
            return self.currentPosition.loc[idx[book_list, ts_code_list], :]

    def updateOrderStatus(self, id_status_tuple_list):
        statement = """
        UPDATE order_book
        SET order_status  = ?
        WHERE order_id = ?
        """
        self.brokerc.executemany(statement, id_status_tuple_list)
        self.brokerconn.commit()

    def updateCurrentPosition(self, userPosition, include_index=True):
        if include_index:
            self.currentPosition = userPosition
        else:
            self.currentPosition = userPosition.set_index(['book', 'ts_code'])

    def updateHistPosition(self, userCurrentPosition):
        userCurrentPosition['trade_date'] = self.current_date
        userCurrentPosition.to_sql('hist_position',
                                   self.brokerconn,
                                   if_exists='append',
                                   index=True,
                                    header = False)

    def updateHistPositionCSV(self, userPosition):
        userPosition['trade_date'] = self.current_date
        if self.flag:
            userPosition.to_csv('hist_position.csv', index=True, mode = 'a', header = True)
            self.flag = False
        else:
            userPosition.to_csv('hist_position.csv', index=True, mode='a', header=False)

    def initialDepositCash(self, book_initial_dict):
        for eachname in book_initial_dict:
            idx = pd.MultiIndex.from_product([[eachname], ['cash']], names=['book', 'ts_code'])
            df = pd.DataFrame([[book_initial_dict[eachname]['cash']]], index = idx, columns=['position'])
            self.currentPosition = pd.concat([self.currentPosition,df])

    def close(self):
        self.brokerconn.close()
