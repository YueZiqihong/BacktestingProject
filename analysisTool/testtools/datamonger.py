from . import generalsupport as gs
import pandas as pd

class Datamonger:
    def __init__ (self):
        self._dbname = "testMarket.db"
        self.mktconn, self.mktc = gs.connectDB(self._dbname)
        self.dataconn = gs.connectTS()

    def getRawDailyMarketData(self, start_date, end_date, stock_pool = None, columns = None):
        columns_str = gs.handleQueryColumnsList(columns)
        start_date = gs.addDashtoDate(start_date)
        end_date = gs.addDashtoDate(end_date)
        stock_list = gs.handleStockPoolType(stock_pool)
        if stock_list is not None:
            tscode_str = gs.handleQueryStockList(stock_pool)
            statement = """
            SELECT {0}
            FROM marketinfo
            WHERE ts_code IN ({1})
        	AND trade_date BETWEEN DATE ('{2}') AND DATE ('{3}')
            """.format(columns_str, tscode_str, start_date, end_date)
        else:
            statement ="""
            SELECT {0}
            FROM marketinfo
            WHERE trade_date >= date('{1}')
            AND trade_date <= date('{2}')
            """.format(columns_str, start_date, end_date)
        return pd.read_sql_query(statement, self.mktconn)

    def getValidTradeDate(self, start_date, end_date):
        return gs.SQLvalidTradeDate(start_date, end_date, self.mktconn)

    def getHuShen300IndexComponent(self):
        statement = """
        SELECT * FROM Hushen300component
        """
        df = pd.read_sql_query(statement, self.mktconn)
        return df

    def close(self):
        self.mktconn.close()
