import sqlite3
import tushare as ts
import pandas as pd
from datetime import datetime
from datetime import timedelta


def execmtSQL(sentence, conn, cursor):
    cursor.execute(sentence)
    conn.commit()


def SQLdescribeTable(tbname, conn, cursor):
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
    print("cwd: " + os.getcwd())
    os.chdir(path)
    print("updated: " + os.getcwd())


def connectDB(dbname):
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
    df = pro.query('adj_factor',  trade_date=date)
    return df


def compareDf(df1, df2):
    pd.concat([df1, df2]).drop_duplicates(keep=False)


def addDashtoDate(date_string):
    date_object = datetime.strptime(date_string, "%Y%m%d")
    new_date_string = datetime.strftime(date_object, "%Y-%m-%d")
    return new_date_string


def removeDashFromDate(date_string):
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
    result = ""
    if len(sample_list) > 1:
        separator = "','"
        result = "'" + separator.join(sample_list) + "'"
    if len(sample_list) == 1:
        result = "'" + str(sample_list[0]) + "'"
    return result


def handleStockPoolType(stock_pool):
    if stock_pool is not None:
        if isinstance(stock_pool, pd.Series):
            stock_pool = stock_pool.tolist()
        elif isinstance(stock_pool, list):
            pass
        else:
            raise TypeError
        return stock_pool
    else:
        return stock_pool


def handleQueryColumnsList(field_list):
    if field_list is not None:
        separator = ","
        result = separator.join(field_list)
        return result
    else:
        return "*"


def handleQueryStockList(stock_list):
    return addCommaQuoteToList(stock_list)


def handleQueryFilterDict(filter_dict):
    start_str = "WHERE "
    middle_str = ""
    flag = False

    for eachFilter in filter_dict:
        if filter_dict[eachFilter] is None or len(filter_dict[eachFilter]) == 0:
            continue
        flag = True
        if eachFilter != 'trade_date':
            middle_str += "{0} IN ({1}) AND\n".format(eachFilter,
                                                      addCommaQuoteToList(filter_dict[eachFilter]))
        if eachFilter == 'trade_date':
            if len(filter_dict['trade_date']) == 1:
                middle_str += "trade_date = date('{0}') AND\n".format(
                    filter_dict['trade_date'][0])
            if len(filter_dict['trade_date']) == 2:
                middle_str += "trade_date >= date('{0}') AND\n trade_date <= date('{1}') AND\n".format(
                    filter_dict['trade_date'][0],
                    filter_dict['trade_date'][1])
    if flag == True:
        return start_str + middle_str[:-5]
    else:
        return ""


def queryGenerator(tbname, column_list=None, filter_dict=None):
    column_str = handleQueryColumnsList(column_list)
    filter_str = handleQueryFilterDict(filter_dict)
    statement = """
    SELECT {0}\nFROM {1}\n{2}
    """.format(column_str, tbname, filter_str)
    return statement


def calculateCommission(deal_total):
    tobroker = max(abs(deal_total * 0.00012), 5)
    if deal_total < 0:
        tax = abs(deal_total) * 0.001
    else:
        tax = 0
    return tobroker + tax


def thisMonthStart():
    now = datetime.now()
    this_month_start = datetime(now.year, now.month, 1)
    this_month_start_str = datetime.strftime(this_month_start, "%Y%m%d")
    return this_month_start_str

def latestDate():
    now = datetime.now()
    yesterday = datetime.strftime(now, "%Y%m%d")
    return yesterday

def nextDate(inputDate_str):    
    inputDate = datetime.strptime(inputDate_str, "%Y-%m-%d")
    nextDate =  inputDate + timedelta(days=1)
    nextDate_str = datetime.strftime(nextDate, "%Y-%m-%d")
    return nextDate_str
