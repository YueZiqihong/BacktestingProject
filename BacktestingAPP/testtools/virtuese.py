# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 12:17:58 2020

@author: zymun
"""
import pandas as pd
import generalsupport as gs
import marketexpress
import brokerdatabase
import pickyinvestor
import monobroker
import time

class VirtueSE:
    def __init__(self):
        # 除非用户设定setStockPool, 否则默认本次不存在股票池, 是针对数据库中的所有股票.
        self.stock_pool = None
        pass
    def setRunningInterval(self, start_date, end_date):
        """
        设置交易的开始和结束日期,并从datamonger对象中获得对应的交易日历
        start_date, end_date: "yyyymmdd"
        """
        self.start_date = gs.addDashtoDate(start_date)
        self.end_date = gs.addDashtoDate(end_date)
        # 设定回测的交易日历
        
    def setStockPool(self, stock_pool = None):
        """
        设定此次回测期间可能交易的股票池以缩小市场备选的数据量(可选)
        stock_pool: Series / List
        """
        # 判断stockpool的类型, 如果是空则返回空list, 若非则输出list类型
        self.stock_pool = gs.handleStockPoolType(stock_pool)
        
    def setStrategy(self):
        self.strategy = pickyinvestor.PickyInvestor()
        
    def createMarketExpressDB(self, mother_db_name, marketexpress_db_name):
        """
        用来初始化本次需要的Market Express 数据库. 目的是加载
        1. 和本次回测时间和股票池有关的市场数据/ 前复权 and 后复权 
        2. 复制相关的交易日历
        3. 创建一个marketnow的临时数据表格
        """
        meconn, mec  = gs.connectDB(marketexpress_db_name)
        # 根据stock_pool决定是否要对其进行filter
        if self.stock_pool is None:
            stock_pool_str = ""
        else:
            stock_pool_str = """AND ts_code IN ({0})""".format(gs.handleQueryStockList(self.stock_pool))
        
        statement  = """
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
            ON backward_market(trade_date);

        DETACH source;
        """.format(
        mother_db_name,
        self.start_date,
        self.end_date,
        stock_pool_str)
        # 提交该statement, 然后关闭连接
        mec.executescript(statement)
        meconn.close()    
        print(statement)
        
    def setMarketExpressDB(self, marketexpress_db_name):
        """
        当已经存在了MarketExpress数据库时, 直接连接, 跳过新建的步骤.

        Parameters
        ----------
        marketexpress_db_name : String
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.marketdb = marketexpress.MarketExpress(marketexpress_db_name)
        
    def setBrokerDB(self, brokerdatabase_name):
        """
        初始化一个Brokerdatabase实例. 对每次回测而言会新建一个数据库记录本次的交易详情.

        Returns
        -------
        None.

        """
        self.brokerdb = brokerdatabase.Brokerdatabase()
        self.brokerdb.createBrokerDatabase(brokerdatabase_name)
        # 新建该数据库之后, 插入hist_position表格
        self.brokerdb.createHistPositionTable()
        # 插入current_position表格
        self.brokerdb.createCurrentPositionTable()
        # 插入order_book表格
        self.brokerdb.createOrderBookTable()
        
    def setTradingBookInfo(self):
        """
        Call Strategy中的用户信息函数, 将结果传递给monobroker对象的addInvestorBooks方法. 随后该信息会通过broker加入到brokerdatabase的current_position表格里作为初始资金.

        Returns
        -------
        None.

        """
        # 从strategy获取本次的trading book信息.
        book_dict = self.strategy.myTradingBooks()
        # 将参数传递给broker对象.
        self.broker.addInvestorBooks(book_dict)
        
    def setTradingCalendar(self):
        """
        在用户已经set开始和结束日期之后, 而且已经连接了这次回测使用的MarketExpress数据库后, 提取出全部的trade_date为一个List, 作为本次回测的Calender. 并且初始化current_date

        Returns
        -------
        None.

        """
        self.trade_cal = self.marketdb.getTradingCalendar(self.start_date, self.end_date)
        
        self.current_date = self.start_date
        
    def setBacktestingPriceEngine(self, how):
        """
        用户设置回测使用前复权还是后复权的价格.
        """
        if how in ['backward', 'forward']:
            self.priceEngine  = how
        else:
            print("只能设置前复权或者后复权!")
        
    def refreshMarketNow(self):
        """
        进入新的一天时, 命令MarketExpress数据库更新今天的MarketNow数据表.
        """
        self.marketdb.updateMarketNow(self.current_date, self.priceEngine)
        
    def setTradingStrategy(self, strategy_instance):
        self.strategy = strategy_instance
        
    def execute(self):
        
        backtest_start = time.time()
        # -- 开始回测前
        self.setTradingCalendar()
        self.broker = monobroker.MonoBroker()
        self.broker.setBrokerDatabase(self.brokerdb)
        self.broker.setMarketDatabase(self.marketdb)
        self.strategy.setBrokerDatabase(self.brokerdb)
        self.strategy.setMarketDatabase(self.marketdb)
        
        # 初始化账户信息
        self.setTradingBookInfo()
        
        # -- 回测开始
        for tradingdate in self.trade_cal:
            loop_start = time.time()
            # 更新日期
            self.current_date = tradingdate
            # 更新今天的marketnow数据表
            self.refreshMarketNow()
            # 传递参数给brokerdatabase和investor
            self.brokerdb.setCurrentDate(tradingdate)
            self.strategy.setCurrentDate(tradingdate)
            
            
            lasting = time.time() - loop_start
            print( self.current_date ,"开盘前耗时" + str(lasting))
            loop_start = time.time()
            
            # 响应开盘
            self.broker.brokerResponseMarketOpen()
            self.strategy.myTradingOpen()
            
            lasting = time.time() - loop_start
            print( "开盘耗时" + str(lasting))
            loop_start = time.time()
            
            
            # 响应盘中
            self.broker.brokerResponseMarketMiddle()
            self.strategy.myTradingIntra()
            # 响应盘后
            self.broker.brokerVectorResponseMarketClose()
            # self.broker.brokerResponseMarketClose()
            self.strategy.myTradingClose()
            
            
            lasting = time.time() - loop_start
            print( "收盘耗时" + str(lasting))
            loop_start = time.time()            
            
            
            # 最后broker盘整
            self.broker.brokerFinishingToday()
            
            lasting = time.time() - loop_start
            print( "盘整耗时" + str(lasting))
            loop_start = time.time()
        
        # -- 回测结束
        # 关闭数据库的连接
        self.brokerdb.close()
        self.marketdb.close()
        
        backtest_end = time.time()
        self.testoutput = backtest_end - backtest_start
        print("整个回测用时", self.testoutput)
        
        