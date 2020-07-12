# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 17:42:00 2020

@author: zymun
"""

import sqlite3
import tushare as ts
import pandas as pd
from datetime import datetime
from datetime import timedelta


def execmtSQL(sentence, conn, cursor):
    cursor.execute(sentence)
    conn.commit()


def SQLdescribeTable(tbname, conn, cursor):
    #    statement = """
    #        SELECT sql
    #        FROM sqlite_master
    #        WHERE name = ?;
    #    """
    statement = """
        PRAGMA table_info({0})
    """.format(tbname)
    cursor.execute(statement)
    conn.commit()
    printFetchall(cursor.fetchall())


def convertDatetime(df, date_colname):
    """
    Convert the datetime column in df from yyyymmdd to yyyy-mm-dd
    Input: df; date_colname(string)
    Output: df
    """
    df[date_colname] = pd.to_datetime(df[date_colname])
    df[date_colname] = df[date_colname].dt.strftime("%Y-%m-%d")
    return df


def confirmWD(path=r'C:\Users\zymunique\Documents\BackTestLib'):
    import os
    print("当前的工作路径为: " + os.getcwd())
    os.chdir(path)
    print("已经更新为: " + os.getcwd())


def connectDB(dbname):
    """
    由于在连接数据库的时候, 如果没有对应的文件, 则会自动创建.
    所以该函数有自动创建新的SQLite数据文件的功能. 若已经有, 则会创建连接.
    """
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    return conn, cursor


def SQLprintTable(tbname, conn, cursor):
    statement = """
        SELECT * FROM {0}
        LIMIT {1} OFFSET 0;
    """.format(tbname, 10)
    cursor.execute(statement)
    conn.commit()
    printFetchall(cursor.fetchall())


def connectTS():
    """
    使用给定的token, 连接Tushare数据端, 返回一个对象pro.
    """
    ts.set_token("440d7b5b33c5bc2d79338862246f26664aa026db00876a8f4e610938")
    pro = ts.pro_api()
    return pro


def printFetchall(cursor):
    for list_ele in cursor.fetchall():
        print(list_ele)


def SQLshowAllTables(conn, cursor):
    execmtSQL("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';",
              conn,
              cursor)
    printFetchall(cursor.fetchall())


def TStradeCal(pro, start_date, end_date):
    df = pro.query('trade_cal', start_date=start_date, end_date=end_date)
    return df


def TSdailyAllPrice(pro, date):
    df = pro.daily(trade_date=date)
    return df


def SQLdeleteRows(tbname, conn, cursor):
    statement = """
    DELETE FROM {0}
    """.format(tbname)
    cursor.execute(statement)
    conn.commit()


def TSdailyAllFactor(pro, date):
    """
    利用Tushare的接口返回某一天的全部股票复权因子.
    返回dataframe.
    """
    df = pro.query('adj_factor',  trade_date=date)
    return df


def compareDf(df1, df2):
    """
    对比两个dataframe的差异, 不返回任何值.
    直接在console中输出单独出现过的行.
    """
    pd.concat([df1, df2]).drop_duplicates(keep=False)


def addDashtoDate(date_string):
    """
    yyyymmdd 格式的日期 转化为 yyyy-mm-dd格式
    """
    date_object = datetime.strptime(date_string, "%Y%m%d")
    new_date_string = datetime.strftime(date_object, "%Y-%m-%d")
    return new_date_string


def removeDashFromDate(date_string):
    """
    yyyy-mm-dd 格式的日期 转化为 yyyymmdd格式
    """
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    new_date_string = datetime.strftime(date_object, "%Y%m%d")
    return new_date_string


def SQLvalidTradeDate(start, end, conn):
    start = addDashtoDate(start)
    end = addDashtoDate(end)
    statement = """
    SELECT trade_date FROM trade_cal
    WHERE trade_date >= date('{0}')
    AND trade_date <= date('{1}')
    AND is_open = 1
    """.format(start, end)
    df = pd.read_sql_query(statement, conn)
    return df['trade_date']


def addCommaQuoteToList(sample_list):
    """
    将List中的每个元素加入单引号和逗号隔开,返回字符串.
    """
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
    # 首先判断是否stock_pool是否为空, 若为空, 则直接返回None.
    # 若instance是一个pandas series, 那么转化为list之后再返回
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


def handleQueryColumnsList(field_list):
    """
    给定一个含有字段名的List, 在其中增加逗号分隔并返回相应的字符串.
    """
    if field_list is not None:
        separator = ","
        result = separator.join(field_list)
        return result
    else:
        return "*"


def handleQueryStockList(stock_list):
    """
    给定含有股票代码的List, 在收尾增加单引号, 之间增加单引号和逗号, 返回字符串
    """
    return addCommaQuoteToList(stock_list)


def handleQueryFilterDict(filter_dict):
    """
    将filter_dict的内容生成一个WHERE statement

    Parameters
    ----------
    filter_dict : Dictionary
    None.

    Returns
    -------
    返回一个String包含WHERE Statement.

    """
    start_str = "WHERE "
    middle_str = ""
    # 是否至少有一个约束条件
    flag = False

    for eachFilter in filter_dict:
        # 如果key对应的value中为None 或者List为空, 说明没有限制条件, 跳过
        if filter_dict[eachFilter] is None or len(filter_dict[eachFilter]) == 0:
            continue
        # 至少有一个约束条件, 则有Where Statement
        flag = True
        if eachFilter != 'trade_date':
            middle_str += "{0} IN ({1}) AND\n".format(eachFilter,
                                                      addCommaQuoteToList(filter_dict[eachFilter]))
        # 如果碰到了对trade_date的处理, 那么需要用>= 和 = 的形式
        if eachFilter == 'trade_date':
            if len(filter_dict['trade_date']) == 1:
                middle_str += "trade_date = date('{0}') AND\n".format(
                    filter_dict['trade_date'][0])
            if len(filter_dict['trade_date']) == 2:
                middle_str += "trade_date >= date('{0}') AND\n trade_date <= date('{1}') AND\n".format(
                    filter_dict['trade_date'][0],
                    filter_dict['trade_date'][1])

    # 如果有约束条件:
    if flag == True:
        return start_str + middle_str[:-5]
    else:
        return ""


def queryGenerator(tbname, column_list=None, filter_dict=None):
    """
    动态生成Select语句的SQL质询SELECT语句.
    """
    # 先处理可选的字段名
    column_str = handleQueryColumnsList(column_list)
    # 处理filter的情况
    filter_str = handleQueryFilterDict(filter_dict)
    statement = """
    SELECT {0}\nFROM {1}\n{2}
    """.format(column_str, tbname, filter_str)
    return statement


def calculateCommission(deal_total):
    """
    计算需要的佣金和税费.
    deal_total可以为任意的正数或者负数的总交易额., 返回一个正数.
    """
    tobroker = max(abs(deal_total * 0.00012), 5)
    if deal_total < 0:
        tax = abs(deal_total) * 0.001
    else:
        tax = 0
    return tobroker + tax


def thisMonthStart():
    """
    返回本月的第一天的日期yyyymmdd
    """
    now = datetime.now()
    this_month_start = datetime(now.year, now.month, 1)
    this_month_start_str = datetime.strftime(this_month_start, "%Y%m%d")
    return this_month_start_str

def latestDate():
    """
    返回昨天的日期, 格式为yyyymmdd
    """
    now = datetime.now()
    yesterday = datetime.strftime(now, "%Y%m%d")
    return yesterday

def nextDate(inputDate_str):
    """
    date_str应该是一个yyyy-mm-dd格式的日期, 返回第二天的yyyy-mm-dd日期
    """
    inputDate = datetime.strptime(inputDate_str, "%Y-%m-%d")
    nextDate =  inputDate + timedelta(days=1)
    nextDate_str = datetime.strftime(nextDate, "%Y-%m-%d")
    return nextDate_str
