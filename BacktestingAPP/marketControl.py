
import pandas as pd
import time
import pandas as pd
from datetime import datetime
# import generalsupport as gs
# import marketexpress
# import brokerdatabase
# import pickyinvestor
# import monobroker


class VirtualMarket:
    def __init__(self):
        self.priceEngine = "backward"
        self.start_date = "20190601"
        self.end_date = "20200601"
        self.cash = 100000
        self.stock_pool = None # 除非用户设定setStockPool, 否则默认本次不存在股票池, 是针对数据库中的所有股票.
        self.strategy = ""

        # 初始化:使用参数（前/后，起始，终止，策略，初始资金（可缺省），股票池（可缺省））。如果报错直接raise。否则：
        # 初始化一个几个小数据表：
        #     trade_calendar是大数据表当中在这个范围内的日期,
        #     backward,forward
        # ；
        #
        # 然后，初始化交易表(brokerdatabase)，其中涉及到初始资金；
        #
        # 把这次回测的所有交易日提取出来，准备开始回测；
        #
        # 回测：

    def setRunningInterval(self, start_date, end_date):
        """
        设置交易的开始和结束日期,并从datamonger对象中获得对应的交易日历
        start_date, end_date: "yyyymmdd"
        """
        self.start_date = addDashtoDate(start_date)
        self.end_date = addDashtoDate(end_date)

    def setStockPool(self, stock_pool = None):
        """
        设定此次回测期间可能交易的股票池以缩小市场备选的数据量(可选)
        stock_pool: PD Series / List
        """
        # 判断stockpool的类型, 如果是空则返回空list, 若非则输出list类型
        self.stock_pool = handleStockPoolType(stock_pool)

    def setBacktestingPriceEngine(self, how):
        """
        用户设置回测使用前复权还是后复权的价格.
        """
        if how in ['backward', 'forward']:
            self.priceEngine  = how
        else:
            print("只能设置前复权或者后复权!")

    def setCash(self, cash):
        self.cash = cash

    def setStrategy(self):
        # self.strategy = pickyinvestor.PickyInvestor()
        pass

    # def createMarketExpressDB(self, mother_db_name, marketexpress_db_name):
    #     """
    #     用来初始化本次需要的Market Express 数据库. 目的是加载
    #     1. 和本次回测时间和股票池有关的市场数据/ 前复权 and 后复权
    #     2. 复制相关的交易日历
    #     3. 创建一个marketnow的临时数据表格
    #     """
    #     meconn, mec  = gs.connectDB(marketexpress_db_name)
    #     # 根据stock_pool决定是否要对其进行filter
    #     if self.stock_pool is None:
    #         stock_pool_str = ""
    #     else:
    #         stock_pool_str = """AND ts_code IN ({0})""".format(gs.handleQueryStockList(self.stock_pool))
    #
    #     statement  = """
    #     ATTACH DATABASE '{0}' AS source;
    #
    #     CREATE TABLE main.trade_cal AS
    #     SELECT trade_date FROM source.trade_cal
    #     WHERE trade_date >= DATE('{1}')
    #     AND trade_date <= DATE('{2}')
    #     AND exchange = 'SSE'
    #     AND is_open = 1
    #     ORDER BY trade_date;
    #
    #     CREATE TABLE main.backward_market AS
    #         SELECT ts_code,
    #     	trade_date,
    #     	open * adj_factor / latest_factor AS open,
    #     	high * adj_factor / latest_factor AS high,
    #     	low * adj_factor / latest_factor AS low,
    #     	close * adj_factor / latest_factor AS close,
    #     	vol,
    #     	pct_chg
    #         FROM (
    #         	SELECT a.ts_code,
    #         		a.trade_date,
    #         		a.open,
    #         		a.high,
    #         		a.low,
    #         		a.close,
    #         		a.vol,
    #         		a.pct_chg,
    #         		a.adj_factor,
    #         		b.adj_factor AS latest_factor
    #         	FROM source.marketinfo a
    #         	LEFT JOIN source.latest_factor b ON a.ts_code = b.ts_code
    #         	)
    #         WHERE trade_date >= DATE('{1}')
    #         AND trade_date <= DATE('{2}')
    #         {3};
    #
    #     CREATE INDEX idx_backward_trade_date
    #         ON backward_market(trade_date);
    #
    #     CREATE TABLE main.forward_market AS
    #         SELECT ts_code,
    #     	trade_date,
    #     	open * adj_factor AS open,
    #     	high * adj_factor AS high,
    #     	low * adj_factor AS low,
    #     	close * adj_factor AS close,
    #     	vol,
    #     	pct_chg
    #         FROM source.marketinfo
    #         WHERE trade_date >= DATE('{1}')
    #         AND trade_date <= DATE('{2}')
    #         {3};
    #
    #      CREATE INDEX idx_forward_trade_date
    #         ON backward_market(trade_date);
    #
    #     DETACH source;
    #     """.format(
    #     mother_db_name,
    #     self.start_date,
    #     self.end_date,
    #     stock_pool_str)
    #     # 提交该statement, 然后关闭连接
    #     mec.executescript(statement)
    #     meconn.close()
    #     print(statement)
    #
    # def setMarketExpressDB(self, marketexpress_db_name):
    #     """
    #     当已经存在了MarketExpress数据库时, 直接连接, 跳过新建的步骤.
    #
    #     Parameters
    #     ----------
    #     marketexpress_db_name : String
    #         DESCRIPTION.
    #
    #     Returns
    #     -------
    #     None.
    #
    #     """
    #     self.marketdb = marketexpress.MarketExpress(marketexpress_db_name)
    #
    # def setBrokerDB(self, brokerdatabase_name):
    #     """
    #     初始化一个Brokerdatabase实例. 对每次回测而言会新建一个数据库记录本次的交易详情.
    #
    #     Returns
    #     -------
    #     None.
    #
    #     """
    #     self.brokerdb = brokerdatabase.Brokerdatabase()
    #     self.brokerdb.createBrokerDatabase(brokerdatabase_name)
    #     # 新建该数据库之后, 插入hist_position表格
    #     self.brokerdb.createHistPositionTable()
    #     # 插入current_position表格
    #     self.brokerdb.createCurrentPositionTable()
    #     # 插入order_book表格
    #     self.brokerdb.createOrderBookTable()
    #
    # def setTradingBookInfo(self):
    #     """
    #     Call Strategy中的用户信息函数, 将结果传递给monobroker对象的addInvestorBooks方法. 随后该信息会通过broker加入到brokerdatabase的current_position表格里作为初始资金.
    #
    #     Returns
    #     -------
    #     None.
    #
    #     """
    #     # 从strategy获取本次的trading book信息.
    #     book_dict = self.strategy.myTradingBooks()
    #     # 将参数传递给broker对象.
    #     self.broker.addInvestorBooks(book_dict)
    #
    # def setTradingCalendar(self):
    #     """
    #     在用户已经set开始和结束日期之后, 而且已经连接了这次回测使用的MarketExpress数据库后, 提取出全部的trade_date为一个List, 作为本次回测的Calender. 并且初始化current_date
    #
    #     Returns
    #     -------
    #     None.
    #
    #     """
    #     self.trade_cal = self.marketdb.getTradingCalendar(self.start_date, self.end_date)
    #
    #     self.current_date = self.start_date
    #
    # def refreshMarketNow(self):
    #     """
    #     进入新的一天时, 命令MarketExpress数据库更新今天的MarketNow数据表.
    #     """
    #     self.marketdb.updateMarketNow(self.current_date, self.priceEngine)
    #
    # def setTradingStrategy(self, strategy_instance):
    #     self.strategy = strategy_instance
    #
    # def execute(self):
    #
    #     backtest_start = time.time()
    #     # -- 开始回测前
    #     self.setTradingCalendar()
    #     self.broker = monobroker.MonoBroker()
    #     self.broker.setBrokerDatabase(self.brokerdb)
    #     self.broker.setMarketDatabase(self.marketdb)
    #     self.strategy.setBrokerDatabase(self.brokerdb)
    #     self.strategy.setMarketDatabase(self.marketdb)
    #
    #     # 初始化账户信息
    #     self.setTradingBookInfo()
    #
    #     # -- 回测开始
    #     for tradingdate in self.trade_cal:
    #         loop_start = time.time()
    #         # 更新日期
    #         self.current_date = tradingdate
    #         # 更新今天的marketnow数据表
    #         self.refreshMarketNow()
    #         # 传递参数给brokerdatabase和investor
    #         self.brokerdb.setCurrentDate(tradingdate)
    #         self.strategy.setCurrentDate(tradingdate)
    #
    #
    #         lasting = time.time() - loop_start
    #         print( self.current_date ,"开盘前耗时" + str(lasting))
    #         loop_start = time.time()
    #
    #         # 响应开盘
    #         self.broker.brokerResponseMarketOpen()
    #         self.strategy.myTradingOpen()
    #
    #         lasting = time.time() - loop_start
    #         print( "开盘耗时" + str(lasting))
    #         loop_start = time.time()
    #
    #
    #         # 响应盘中
    #         self.broker.brokerResponseMarketMiddle()
    #         self.strategy.myTradingIntra()
    #         # 响应盘后
    #         self.broker.brokerVectorResponseMarketClose()
    #         # self.broker.brokerResponseMarketClose()
    #         self.strategy.myTradingClose()
    #
    #
    #         lasting = time.time() - loop_start
    #         print( "收盘耗时" + str(lasting))
    #         loop_start = time.time()
    #
    #
    #         # 最后broker盘整
    #         self.broker.brokerFinishingToday()
    #
    #         lasting = time.time() - loop_start
    #         print( "盘整耗时" + str(lasting))
    #         loop_start = time.time()
    #
    #     # -- 回测结束
    #     # 关闭数据库的连接
    #     self.brokerdb.close()
    #     self.marketdb.close()
    #
    #     backtest_end = time.time()
    #     self.testoutput = backtest_end - backtest_start
    #     print("整个回测用时", self.testoutput)
    #




# import sqlite3
# import tushare as ts


# def execmtSQL(sentence, conn, cursor):
#     cursor.execute(sentence)
#     conn.commit()
#
# def SQLdescribeTable(tbname, conn, cursor):
# #    statement = """
# #        SELECT sql
# #        FROM sqlite_master
# #        WHERE name = ?;
# #    """
#     statement = """
#         PRAGMA table_info({0})
#     """.format(tbname)
#     cursor.execute(statement)
#     conn.commit()
#     printFetchall(cursor.fetchall())
#
# def convertDatetime(df, date_colname):
#     """
#     Convert the datetime column in df from yyyymmdd to yyyy-mm-dd
#     Input: df; date_colname(string)
#     Output: df
#     """
#     df[date_colname] = pd.to_datetime(df[date_colname])
#     df[date_colname] = df[date_colname].dt.strftime("%Y-%m-%d")
#     return df
#
# def createDB(dbname):
#     """
#     Create a databse given name and return the connection, cursor bar.
#     Output: connection, cursor object
#     """
#     conn = sqlite3.connect(dbname)
#     c = conn.cursor()
#     return conn, c
#
# def confirmWD(path = r'C:\Users\zymunique\Documents\BackTestLib'):
#     import os
#     print("当前的工作路径为: " + os.getcwd())
#     os.chdir(path)
#     print("已经更新为: " + os.getcwd())
#
# def connectDB(dbname):
#     conn = sqlite3.connect(dbname)
#     cursor = conn.cursor()
#     return conn, cursor
#
# def SQLprintTable(tbname, conn, cursor):
#     statement = """
#         SELECT * FROM {0}
#         LIMIT {1} OFFSET 0;
#     """.format(tbname, 10)
#     cursor.execute(statement)
#     conn.commit()
#     printFetchall(cursor.fetchall())
#
# def connectTS():
#     ts.set_token("440d7b5b33c5bc2d79338862246f26664aa026db00876a8f4e610938")
#     pro = ts.pro_api()
#     return pro
#
# def printFetchall(cursor):
#     for list_ele in cursor.fetchall():
#         print(list_ele)
#
# def SQLshowAllTables(conn, cursor):
#     execmtSQL("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';" ,
#               conn,
#               cursor)
#     printFetchall(cursor.fetchall())
#
# def TStradeCal(pro, start_date, end_date):
#     df = pro.query('trade_cal', start_date = start_date, end_date = end_date)
#     return df
#
# def TSdailyAllPrice(pro, date):
#     df =  pro.daily(trade_date = date)
#     return df
#
# def SQLdeleteRows(tbname, conn, cursor):
#     statement = """
#     DELETE FROM {0}
#     """.format(tbname)
#     cursor.execute(statement)
#     conn.commit()
#
# def TSdailyAllFactor(pro, date):
#     df = pro.query('adj_factor',  trade_date=date)
#     return df
#
# def compareDf(df1, df2):
#     pd.concat([df1, df2]).drop_duplicates(keep = False)

def addDashtoDate(date_string):
    date_object = datetime.strptime(date_string, "%Y%m%d")
    new_date_string = datetime.strftime(date_object, "%Y-%m-%d")
    return new_date_string

# def removeDashFromDate(date_string):
#     date_object = datetime.strptime(date_string, "%Y-%m-%d")
#     new_date_string = datetime.strftime(date_object, "%Y%m%d")
#     return new_date_string
#
# def SQLvalidTradeDate(start, end, conn):
#     start = addDashtoDate(start)
#     end = addDashtoDate(end)
#     statement = """
#     SELECT trade_date FROM trade_cal
#     WHERE trade_date >= date('{0}')
#     AND trade_date <= date('{1}')
#     AND is_open = 1
#     """.format(start, end)
# #    print(statement)
#     df = pd.read_sql_query(statement, conn)
#     return df['trade_date']
#
# def addCommaQuoteToList(sample_list):
    result = ""
    if len(sample_list) > 1:
        separator = "','"
        result = "'" + separator.join(sample_list) + "'"
    if len(sample_list) == 1:
        result = "'" + str(sample_list[0]) + "'"
    return result

def handleStockPoolType(stock_pool):
    """
    保证返回的stockpool是一个List类型
    stock_pool: Series, List, None
    Output: List / None
    """
    if stock_pool is not None:
        if isinstance(stock_pool, pd.Series):
            stock_pool = stock_pool.tolist()
        elif isinstance(stock_pool, list):
            pass
        else:
            print("输入的stock_pool变量不是Series或List类型!")
            raise TypeError
        return stock_pool
    else:
        return stock_pool

# def handleQueryColumnsList(field_list):
#     """
#     给定一个含有字段名的List, 在其中增加逗号分隔并返回相应的字符串.
#     """
#     if field_list is not None:
#         separator = ","
#         result = separator.join(field_list)
#         return result
#     else:
#         return "*"
#
# def handleQueryStockList(stock_list):
#     """
#     给定含有股票代码的List, 在收尾增加单引号, 之间增加单引号和逗号, 返回字符串
#     """
#     return addCommaQuoteToList(stock_list)
#
# def handleQueryFilterDict(filter_dict):
#     """
#     将filter_dict的内容生成一个WHERE statement
#
#     Parameters
#     ----------
#     filter_dict : Dictionary
#     None.
#
#     Returns
#     -------
#     返回一个String包含WHERE Statement.
#
#     """
#     start_str = "WHERE "
#     middle_str = ""
#     # 是否至少有一个约束条件
#     flag = False
#
#     for eachFilter in filter_dict:
#         # 如果key对应的value中为None 或者List为空, 说明没有限制条件, 跳过
#         if filter_dict[eachFilter] is None or len(filter_dict[eachFilter]) == 0:
#             continue
#         # 至少有一个约束条件, 则有Where Statement
#         flag = True
#         if eachFilter != 'trade_date':
#             middle_str += "{0} IN ({1}) AND\n".format(eachFilter, addCommaQuoteToList(filter_dict[eachFilter]))
#         # 如果碰到了对trade_date的处理, 那么需要用>= 和 = 的形式
#         if eachFilter == 'trade_date':
#             if len(filter_dict['trade_date']) == 1:
#                 middle_str += "trade_date = date('{0}') AND\n".format(filter_dict['trade_date'][0])
#             if len(filter_dict['trade_date']) == 2:
#                 middle_str += "trade_date >= date('{0}') AND\n trade_date <= date('{1}') AND\n".format(
#                     filter_dict['trade_date'][0],
#                     filter_dict['trade_date'][1])
#
#     # 如果有约束条件:
#     if flag == True:
#         return start_str + middle_str[:-5]
#     else:
#         return ""
#
# def queryGenerator(tbname, column_list = None, filter_dict = None):
#     """
#     动态生成Select语句的SQL质询
#     """
#     # 先处理可选的字段名
#     column_str = handleQueryColumnsList(column_list)
#     # 处理filter的情况
#     filter_str = handleQueryFilterDict(filter_dict)
#     statement = """
#     SELECT {0}\nFROM {1}\n{2}
#     """.format(column_str, tbname, filter_str)
#     return statement
#
# def calculateCommission(deal_total):
#     """
#     计算需要的佣金和税费.
#     deal_total可以为任意的正数或者负数的总交易额., 返回一个正数.
#     """
#     tobroker = max(abs(deal_total * 0.00012), 5)
#     if deal_total < 0:
#         tax = abs(deal_total) * 0.001
#     else:
#         tax = 0
#     return tobroker + tax
#
# def thisMonthStart():
#     """
#     返回本月的第一天的日期yyyymmdd
#     """
#     now = datetime.now()
#     this_month_start = datetime(now.year, now.month, 1)
#     this_month_start_str = datetime.strftime(this_month_start, "%Y%m%d")
#     return this_month_start_str
