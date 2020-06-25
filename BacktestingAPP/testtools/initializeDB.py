# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 19:34:06 2020

@author: zymun
"""

import sqlite3
import tushare as ts
import pandas as pd
from datetime import datetime
import generalsupport as gs

def SQLcreateMarketTable(conn, cursor):
    statement = """
        CREATE TABLE marketinfo
        (
        ts_code	VARCHAR(12)	NOT NULL,
        trade_date	DATE	NOT NULL,
        open	FLOAT,
        high	FLOAT,
        low		FLOAT,
        close	FLOAT,
        vol	FLOAT,
        pct_chg FLOAT,
        adj_factor FLOAT,
        PRIMARY KEY (ts_code, trade_date)
        )
    """
    gs.execmtSQL(statement, conn, cursor)
    
def SQLcreateTradeCalTable(conn, cursor):
    statement = """
    CREATE TABLE trade_cal
    (
    exchange VARCHAR(6),
    trade_date DATE,
    is_open BOOLEAN,
    PRIMARY KEY(exchange, trade_date)
    )
    """
    cursor.execute(statement)
    conn.commit()