from . import generalsupport as gs
import pandas as pd


class MarketExpress():
    def __init__(self, dbname):
        self.expconn, self.expc = gs.connectDB(dbname)
        self.backDataTable = 'backward_market'
        self.forwardDataTable = 'forward_market'

    def getBackMarketData(self, column_list=None, filter_dict=None):
        statement = gs.queryGenerator(self.backDataTable,
                                      column_list,
                                      filter_dict)
        return pd.read_sql_query(statement, self.expconn)

    def getFowardMarketData(self, column_list=None, filter_dict=None):
        statement = gs.queryGenerator(self.forwardDataTable,
                                      column_list,
                                      filter_dict)
        return pd.read_sql_query(statement, self.expconn)

    def getMarketNow(self, column_list=None, filter_dict=None):
        return self.marketnow

    def getTradingCalendar(self, start_date, end_date):
        statement = gs.queryGenerator('trade_cal',
                                      None,
                                      {'trade_date': [start_date, end_date]})
        df = pd.read_sql_query(statement, self.expconn)
        return df['trade_date'].tolist()

    def updateMarketNow(self, date, how):
        if how == "backward":
            table_name = "backward_market"
        if how == "forward":
            table_name = "forward_market"
        statement = """
        SELECT * FROM {0}
        WHERE trade_date = DATE('{1}');
        """.format(table_name, date)
        self.marketnow = pd.read_sql_query(statement, self.expconn)

    def close(self):
        self.expconn.close()
