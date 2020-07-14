from . import generalsupport as gs
from . import marketexpress
from . import brokerdatabase
from . import pickyinvestor
from . import monobroker

import time
import pandas as pd
import logging
import os

class VirtualSE:
    def __init__(self):
        self.stock_pool = None

    def startLogger(self):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename='example.log',
                    level=logging.DEBUG,
                    format='%(asctime)-30s %(relativeCreated)-10d %(message)s')

    def setRunningInterval(self, start_date, end_date):
        self.start_date = gs.addDashtoDate(start_date)
        self.end_date = gs.addDashtoDate(end_date)

    def setStockPool(self, stock_pool=None):
        self.stock_pool = gs.handleStockPoolType(stock_pool)

    def setStrategy(self):
        self.strategy = pickyinvestor.PickyInvestor()

    def createMarketExpressDB(self, mother_db_name, marketexpress_db_name):
        meconn, mec = gs.connectDB(marketexpress_db_name)
        if self.stock_pool is None:
            stock_pool_str = ""
        else:
            stock_pool_str = """AND ts_code IN ({0})""".format(
                gs.handleQueryStockList(self.stock_pool))

        statement = """
        ATTACH DATABASE '{0}' AS source;

        CREATE TABLE main.trade_cal AS
        SELECT trade_date FROM source.trade_cal
        WHERE trade_date >= DATE('{1}')
        AND trade_date <= DATE('{2}')
        AND exchange = 'SSE'
        AND is_open = 1
        ORDER BY trade_date;

        CREATE TABLE main.backward_market AS
            SELECT ts_code,
        	trade_date,
        	open * adj_factor / latest_factor AS open,
        	high * adj_factor / latest_factor AS high,
        	low * adj_factor / latest_factor AS low,
        	close * adj_factor / latest_factor AS close,
        	vol,
        	pct_chg
            FROM (
            	SELECT a.ts_code,
            		a.trade_date,
            		a.open,
            		a.high,
            		a.low,
            		a.close,
            		a.vol,
            		a.pct_chg,
            		a.adj_factor,
            		b.adj_factor AS latest_factor
            	FROM source.marketinfo a
            	LEFT JOIN source.latest_factor b ON a.ts_code = b.ts_code
            	)
            WHERE trade_date >= DATE('{1}')
            AND trade_date <= DATE('{2}')
            {3};

        CREATE INDEX idx_backward_trade_date
            ON backward_market(trade_date);

        CREATE TABLE main.forward_market AS
            SELECT ts_code,
        	trade_date,
        	open * adj_factor AS open,
        	high * adj_factor AS high,
        	low * adj_factor AS low,
        	close * adj_factor AS close,
        	vol,
        	pct_chg
            FROM source.marketinfo
            WHERE trade_date >= DATE('{1}')
            AND trade_date <= DATE('{2}')
            {3};

         CREATE INDEX idx_forward_trade_date
            ON forward_market(trade_date);

        DETACH source;
        """.format(
            mother_db_name,
            self.start_date,
            self.end_date,
            stock_pool_str)
        mec.executescript(statement)
        meconn.close()
        print(statement)

    def setMarketExpressDB(self, marketexpress_db_name):
        self.marketdb = marketexpress.MarketExpress(marketexpress_db_name)

    def setBrokerDB(self, brokerdatabase_name):
        if os.path.isfile(brokerdatabase_name):
            os.remove(brokerdatabase_name)
            logging.debug("Database named {0} already exists and will be deleted.".format(brokerdatabase_name))

        self.brokerdb = brokerdatabase.Brokerdatabase()
        self.brokerdb.createBrokerDatabase(brokerdatabase_name)
        self.brokerdb.createHistPositionTable()
        self.brokerdb.createCurrentPositionTable()
        self.brokerdb.createOrderBookTable()

    def setTradingBookInfo(self):
        book_dict = self.strategy.myTradingBooks()
        self.broker.addInvestorBooks(book_dict)

    def setTradingCalendar(self):
        self.trade_cal = self.marketdb.getTradingCalendar(
            self.start_date, self.end_date)
        self.current_date = self.start_date

    def setBacktestingPriceEngine(self, how):
        self.priceEngine = how

    def refreshMarketNow(self):
        self.marketdb.updateMarketNow(self.current_date, self.priceEngine)

    def setTradingStrategy(self, strategy_instance):
        self.strategy = strategy_instance

    def execute(self):
        self.setTradingCalendar()
        self.broker = monobroker.MonoBroker()
        self.broker.setBrokerDatabase(self.brokerdb)
        self.broker.setMarketDatabase(self.marketdb)
        self.strategy.setBrokerDatabase(self.brokerdb)
        self.strategy.setMarketDatabase(self.marketdb)

        self.startLogger()
        logging.info("Backtesting Initiated...")
        self.setTradingBookInfo()

        for tradingdate in self.trade_cal:
            logging.info("Trade day {0}".format(tradingdate))
            self.current_date = tradingdate
            self.refreshMarketNow()
            self.brokerdb.setCurrentDate(tradingdate)
            self.strategy.setCurrentDate(tradingdate)
            logging.info("Data today loaded successfully.")

            self.broker.brokerResponseMarketOpen()
            self.strategy.myTradingOpen()
            logging.info("End of market open.")
            self.broker.brokerResponseMarketMiddle()
            self.strategy.myTradingIntra()
            logging.info("End of market day.")
            self.broker.brokerVectorResponseMarketClose()
            self.strategy.myTradingClose()
            logging.info("End of after market actions.")
            self.broker.brokerFinishingToday()
            logging.info("Market close. Data updated.")
        self.brokerdb.close()
        self.marketdb.close()
        logging.shutdown()

    def getTransactionData(self):
        return open("hist_position.csv")

    def clear(self):
        """
        Clean up temp files.
        """
        os.remove("aTest.db")
        os.remove("hist_position.csv")
        # os.remove("example.log")
        # os.remove("externalDB.DB")
