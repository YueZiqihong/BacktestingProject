import numpy as np
import pandas as pd
import time
import datetime
import random

from .models import *
from django.db import connection
from django_pandas.io import read_frame
from django.db import transaction


class VirtualMarket:
    def __init__(self):
        self.priceEngine = "backward"
        self.start_date = datetime.date(2019,6,5)
        self.end_date = datetime.date(2020,6,1)
        self.stock_pool = None # 除非用户设定setStockPool, 否则默认本次不存在股票池, 是针对数据库中的所有股票.
        self.strategy = Strategy()
        self.strategy.setBook(10000)
        self.broker = Broker()
        # 初始化:使用参数（前/后，起始，终止，策略，初始资金（可缺省），股票池（可缺省））。如果报错直接raise

    def setRunningInterval(self, start_date, end_date):
        """
        设置交易的开始和结束日期,并从datamonger对象中获得对应的交易日历
        start_date, end_date: "yyyymmdd"
        """
        pass

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

    def setStrategy(self):
        pass

    def updateMarketNow(self,TradeDay):
        """
        给定一个日期, MarketNow数据表刷新为当天的数据. 采用how的方式.
        how可以选择forward 或者 backward.
        """
        Marketnow.objects.all().delete()
        if self.priceEngine == "backward":
            qs = BackwardMarket.objects.filter(trade_day=TradeDay.id)
        if self.priceEngine == "forward":
            qs = BackwardMarket.objects.filter(trade_day=TradeDay.id)
        Marketnow.objects.bulk_create(qs)

    def initializeBacktesting(self):
        OrderBook.objects.all().delete()
        HistPosition.objects.all().delete()
        CurrentPosition.objects.all().delete()

        bookList = []
        for accName in self.strategy.book:
            bookList.append(CurrentPosition(
            book = accName,
            ts_code = "cash",
            position = self.strategy.book[accName]
            ))
        CurrentPosition.objects.bulk_create(bookList)

    def execute(self):
        backtest_start = time.time()
        self.initializeBacktesting()

        for TradeDay in self.calandar:
            pass
            self.updateMarketNow(TradeDay)
            self.strategy.setCurrentDate(TradeDay)
            self.broker.setCurrentDate(TradeDay)

            self.broker.brokerResponseMarketOpen()
            orders = self.strategy.executeTradeOpen()
            OrderBook.objects.bulk_create(orders)

            self.broker.brokerResponseMarketMiddle()
            orders = self.strategy.executeTradeIntra()
            OrderBook.objects.bulk_create(orders)

            self.broker.brokerResponseMarketClose()
            orders = self.strategy.executeTradeClose()
            OrderBook.objects.bulk_create(orders)

            # 最后broker盘整
            # self.broker.brokerFinishingToday()
        # -- 回测结束
        backtest_end = time.time()
        return backtest_end - backtest_start



class Strategy:
    # private
    def __init__(self):
        pass

    def setCurrentDate(self,Day):
        self.currentDay = Day

    def setBook(self,cash):
        self.book = {"a": 200000, "b": 100000}

    # public interface
    def getCurrentDate(self):
        return self.currentDay.trade_date

    def getMarketInfo(self):
        pass

    def getPosition(self):
        pass

    def makeMarketOrderByValue(self,book,ticker,amount):
        self.orders.append(OrderBook(
            book = book,
            ts_code = ticker,
            order_type = "market",
            amount = amount,
            amount_type = "value",
            order_status = "pending",
            trade_day_id = self.currentDay.id
        ))

    def makeMarketOrderByShares(self,book,ticker,amount):
        self.orders.append(OrderBook(
            book = book,
            ts_code = ticker,
            order_type = "market",
            amount = amount,
            amount_type = "shares",
            order_status = "pending",
            trade_day_id = self.currentDay.id
        ))

    def makeLimitOrderByValue(self,book,ticker,amount,price,validity_term):
        self.orders.append(OrderBook(
            book = book,
            ts_code = ticker,
            order_type = "limit",
            limit_price = price,
            amount = amount,
            amount_type = "value",
            validity_term = validity_term,
            order_status = "pending",
            trade_day_id = self.currentDay.id
        ))

    def makeLimitOrderByShares(self,book,ticker,amount,price,validity_term):
        self.orders.append(OrderBook(
            book = book,
            ts_code = ticker,
            order_type = "limit",
            limit_price = price,
            amount = amount,
            amount_type = "shares",
            validity_term = validity_term,
            order_status = "pending",
            trade_day_id = self.currentDay.id
        ))

    # public useredit
    def executeTradeOpen(self):
        self.orders = []
        self.makeMarketOrderByShares("a","000830.SZ",(random.random()-0.5)*100)
        return self.orders

    def executeTradeIntra(self):
        pass

    def executeTradeClose(self):
        pass

class Broker:
    def __init__(self):
        pass

    def setCurrentDate(self,Day):
        self.currentDay = Day

    def getCurrentDate(self):
        return self.currentDay.trade_date

    def readMarketPendingOrder(self):
        qs = OrderBook.objects.filter(
        order_status = "pending",
        order_type = "market"
        )
        qs_dataframe = read_frame(qs=qs,index_col='order_id')
        return qs_dataframe

    def readLimitPendingOrder(self):
        qs = OrderBook.objects.filter(
        order_status = "pending",
        order_type = "limit"
        )
        qs_dataframe = read_frame(qs=qs, index_col='order_id')
        return qs_dataframe

    def readCurrentPosition(self):
        qs = CurrentPosition.objects.all()
        return read_frame(qs)

    def getMarketNow(self, ticker_list):
        qs = Marketnow.objects.filter(ts_code__in=ticker_list)
        return read_frame(qs)

    def vectorizedHandleMarketOrder(self, userPosition, daily_price, order_book):
        """
        向量化的处理市价单.
        userPosition 没有设置index的原生数据表.
        daily_price 只包含ts_code 和 price两列
        order_book 原生的pending_orders Market

        """
        userPosition.set_index(['book','ts_code'], inplace = True)
        # 先合并价格和order_book
        order_book = pd.merge(order_book, daily_price, how = 'left', on = 'ts_code')

        # 计算order_shares, 把value下单的部分转化为股票数的担子
        order_book['amount'] = np.where(order_book['amount_type'] == 'value', np.floor_divide(order_book['amount'], order_book['price']), order_book['amount'])

        # 计算order_amount
        order_amount = (order_book['amount_type'].values == 'shares') * 1 * order_book['amount'].values * order_book['price'].values

        # 计算衍生出来的税费
        broker_fee = np.maximum(np.abs(order_amount) * 0.00012, np.full_like(order_amount , 5))
        broker_tax = np.abs(np.minimum(order_amount * 0.001, np.full_like(order_amount, 0)))
        total_transaction_cost = broker_fee + broker_tax

        # 计算总的payoff
        order_cost = order_amount + total_transaction_cost

        # 按照账户名称和order_cost排序
        order_book['order_cost'] = order_cost
        order_book = order_book.sort_values(by = ['book', 'order_cost'])

        # 创建总的更新序列
        updated_order_status = np.array([])

        for each_book in np.unique(order_book['book'].values):
            # 获取这个账户的order_book
            this_book_order_book = order_book[order_book['book'] == each_book]
            # 如果这个账户没有订单, 那么直接处理下一个账户.
            if this_book_order_book.empty:
                continue
            # 首先找到账户剩余的现金
            cash_available = userPosition.loc[(each_book, 'cash'), 'position']
            # 和该账户相关的order的累计执行成本
            order_cost_cumsum = np.cumsum(this_book_order_book['order_cost'].values)
            # 假定用当前的现金按顺序累计执行, 会剩余多少钱?
            assume_order_complete = cash_available - order_cost_cumsum
            # 更新订单状态, 大于等于0的可以被成功执行, 否则会失败
            order_status_this_book = np.full(assume_order_complete.shape, 'pending')
            # 把没有今天价格的订单设置为-1
            assume_order_complete[np.isnan(assume_order_complete)] = -1
            order_status_this_book = np.where(assume_order_complete >= 0, 'Success', 'Not Enough Cash')
            # 对-1的值, 证明没有价格, 返回其他信息(这里是一个妥协)
            order_status_this_book[assume_order_complete == -1] = "No Price Available"
            # 计算剩余的现金
            # 再剩余的累加中, 寻找大于0的最小值. 也就是剩余的现金.
            cash_after = np.min(assume_order_complete[assume_order_complete >= 0])
            updated_order_status = np.append(updated_order_status, order_status_this_book)
            # 更新现金
            userPosition.loc[(each_book, 'cash'), 'position'] = cash_after

        # 把更新的订单状态赋值给order_book
        order_book['order_status'] = updated_order_status
        # 从而可以传出更新order_status的List of tuple
        order_status_tobereturned = order_book[['order_status', 'order_id']].to_records(index = False).tolist()

        # 下面就是更复杂的更新仓位啦!
        # 用集合操作把没有建仓的账户股票组合找出来, 然后将表格append上去.
        order_book_index_set = set(order_book[order_book['order_status'] == 'Success'][['book', 'ts_code']].to_records(index = False).tolist())
        position_index_set = set(userPosition.index.tolist())

        whatsnewposition = order_book_index_set.difference(position_index_set)

        # 如果这个集合不是空的, 说明userPosition需要加入新的行.
        if bool(whatsnewposition):
            index = pd.MultiIndex.from_tuples(list(whatsnewposition))
            append_df = pd.DataFrame(0, index, columns = userPosition.columns)
            userPosition = userPosition.append(append_df)

        # 合并userPosition和order_book.
        # 从orderbook中筛选出有用的信息, 已经成功的交易单
        temp_order_book = order_book[order_book['order_status'] == 'Success'][['book', 'ts_code', 'amount', 'order_cost']]
        # 保证同一个book和同一个ts_code只有一个记录.
        temp_order_book.groupby(['book','ts_code']).sum()
        # 合并仓位表格和order_book
        calculation_df = pd.merge(userPosition, temp_order_book, how = 'left', on = ['book', 'ts_code']).fillna(0)
        userPosition = userPosition.fillna(0)

        position_after_trade = userPosition['position'].values + calculation_df['amount'].values

        userPosition['wavg_cost'] = np.where(position_after_trade == 0 , 0, (userPosition['wavg_cost'].values * userPosition['position'].values + calculation_df['order_cost'].values) / position_after_trade)

        userPosition['position'] = userPosition['position'].values + calculation_df['amount'].values

        return order_status_tobereturned, userPosition

    def updateOrderStatus(self,statements):
        with transaction.atomic():
            for statement in statements:
                changedOrder = OrderBook.objects.get(order_id=statement[1])
                changedOrder.order_status = statement[0]
                changedOrder.save()

    def updateCurrentPosition(self,userPosition):
        """# WARNING: hardcode"""
        userPosition.to_sql(
        "BacktestingAPP_currentposition",
        connection,
        if_exists = 'replace',
        index = true)

    def brokerResponseMarketOpen(self):
        """
        处理每天的开盘阶段.
        """
        # 获取三大表格, 当前持仓, 今日市场和pendingMarketOrder
        # pendingMarketOrder = self.readMarketPendingOrder()
        # 如果pendingMarketOrder没有任何交易的话..直接退出函数
        # if pendingMarketOrder.empty:
        #     return None
        # userPosition = self.readCurrentPosition()
        # # 获取可能要使用的股票池
        # stock_pool_list = pendingMarketOrder['ts_code'].unique().tolist()
        # stock_pool_price = self.getMarketNow(stock_pool_list)
        # stock_pool_price.rename(columns={'open' : 'price'}, inplace = True)
        #
        # update_order_status_list, userPosition = self.vectorizedHandleMarketOrder(userPosition, stock_pool_price, pendingMarketOrder)
        #
        # "这底下两个要改，但是上头是对的"

        # 更新order status
        # self.updateOrderStatus(update_order_status_list)
        # 更新当前的仓位
        # self.updateCurrentPosition(userPosition)
        pass

    def brokerResponseMarketMiddle(self):
        pass

    def brokerResponseMarketClose(self):
        pass


def initializeContainer(request, market):
    BackwardMarket.objects.all().delete()
    ForwardMarket.objects.all().delete()

    validDates = TradeCalendar.objects.filter(
        trade_date__range=(market.start_date,market.end_date),
        exchange = "SSE",
        is_open = 1
    ).order_by("trade_date")
    market.calandar = validDates

    startDateID = validDates[0].id
    endDateID = validDates[len(validDates)-1].id

    with connection.cursor() as cursor:
        statement = """
        INSERT INTO main.BacktestingAPP_backwardmarket
        (ts_code,open,close,high,low,vol,pct_chg,trade_day_id)
        SELECT
        a.ts_code,
        a.open * a.adj_factor / b.adj_factor,
        a.close * a.adj_factor / b.adj_factor,
        a.high * a.adj_factor / b.adj_factor,
        a.low * a.adj_factor / b.adj_factor,
        a.vol,
        a.pct_chg,
        a.trade_day_id
        FROM main.BacktestingAPP_marketinfo a
        LEFT JOIN main.BacktestingAPP_latestfactor b
        ON a.ts_code = b.ts_code
        WHERE
        a.trade_day_id >= %s AND a.trade_day_id <= %s;"""
        cursor.execute(statement, [startDateID, endDateID])

        statement = """
        INSERT INTO main.BacktestingAPP_forwardmarket
        (ts_code,open,close,high,low,vol,pct_chg,trade_day_id)
        SELECT
        ts_code,
        open * adj_factor,
        close * adj_factor,
        high * adj_factor,
        low * adj_factor,
        vol,
        pct_chg,
        trade_day_id
        FROM main.BacktestingAPP_marketinfo
        WHERE
        trade_day_id >= %s AND trade_day_id <= %s;
        """
        cursor.execute(statement, [startDateID, endDateID])

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
#
# def addDashtoDate(date_string):
#     date_object = datetime.strptime(date_string, "%Y%m%d")
#     new_date_string = datetime.strftime(date_object, "%Y-%m-%d")
#     return new_date_string
#
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
#     result = ""
#     if len(sample_list) > 1:
#         separator = "','"
#         result = "'" + separator.join(sample_list) + "'"
#     if len(sample_list) == 1:
#         result = "'" + str(sample_list[0]) + "'"
#     return result

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
