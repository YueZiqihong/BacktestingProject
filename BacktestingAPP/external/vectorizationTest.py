# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 13:42:48 2020

@author: zymunique
"""

import pandas as pd
import numpy as np

# 目标: 用向量化的方法处理订单.
# 首先获取三大表格.

userPosition = pd.read_csv("current_position.csv")
daily_price = pd.read_csv("marketnow.csv")[['ts_code','close']]
order_book = pd.read_csv("order_book.csv")


vectorizedHandleMarketOrder(userPosition, daily_price, order_book)

def vectorizedHandleMarketOrder(userPosition, daily_price, order_book):

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
    order_status_tobereturned = order_book[['order_id', 'order_status']].to_records(index = False).tolist()
    
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

