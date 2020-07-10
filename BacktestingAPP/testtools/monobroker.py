# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:40:00 2020

@author: zymunique
"""

from . import generalsupport as gs
from . import brokerdatabase as bd
from . import marketexpress as me
import pandas as pd
import numpy as np
import logging


class MonoBroker:
    def __init__(self):
        pass

    def setBrokerDatabase(self, db_instance):
        self.brokerdb = db_instance

    def setMarketDatabase(self, db_instance):
        self.marketdb = db_instance

    def handleSingleMarketOrder(self, book, ts_code, amount, amount_type, df_stock_price, df_user_position, marketPhase):
        """
        执行某一个Market Order.
        Parameters
        ----------
        book : String
            交易的账户名.
        ts_code : String
            交易的股票代码.
        amount : Integer / Float
            交易的数量或者金额.
        amount_type : String
            交易数量还是金额?
        df_stock_price : DataFrame
            所有交易涉及股票的当日价格.
        df_user_position : DataFrame
            将要被引用和修改的用户持仓数据表.
        marketPhase : String
            当天交易的阶段, open, close等.

        Returns
        -------
        str
            当前单子的处理结果, Success / Not Enough Money.
        df_user_position : DataFrame
            处理后的用户持仓数据表.

        """

        try:
            stock_price = df_stock_price.loc[ts_code, marketPhase]
        except KeyError:
            return "No Price Available", df_user_position

        # 判断当前交易需要的费用, 暂时假定没有滑点
        if amount_type == "shares":
            deal_shares = amount
            deal_total = amount * stock_price
            deal_commission = gs.calculateCommission(deal_total)
            deal_cost = deal_total + deal_commission
        else:
            deal_shares = int(amount / stock_price)
            deal_total = deal_shares * stock_price
            deal_commission = gs.calculateCommission(deal_total)
            deal_cost = deal_total + deal_commission
        # 判断是否能够成交?
        if_deal_finish = df_user_position.loc[(
            book, 'cash'), 'position'] - deal_cost
        # 如果成交了
        if if_deal_finish >= 0:
            # 修改当前的现金
            df_user_position.loc[(book, 'cash'), 'position'] = if_deal_finish
            # 修改股票的position 和 average_cost
            # 若股票已经在userPosition中
            if (book, ts_code) in df_user_position.index:
                # 如果不是清仓的情况下, 计算平均成本
                if df_user_position.loc[(book, ts_code), 'position'] + deal_shares != 0:
                    # 计算并更新wavg_cose
                    df_user_position.loc[(book, ts_code), 'wavg_cost'] = (df_user_position.loc[(book, ts_code), 'wavg_cost'] * df_user_position.loc[(
                        book, ts_code), 'position'] + deal_cost) / (df_user_position.loc[(book, ts_code), 'position'] + deal_shares)
                # 否则设置为0.
                else:
                    df_user_position.loc[(book, ts_code), 'wavg_cost'] = 0
                    pass
                # 修改Position的数据
                df_user_position.loc[(book, ts_code),
                                     'position'] += deal_shares
            # 如果股票不在, 需要append
            else:
                df = pd.DataFrame([[deal_shares, None, deal_cost / deal_shares, None, None]], columns=[
                                  'position', 'value', 'wavg_cost', 'return', 'pct_return'], index=[(book, ts_code)])
                df_user_position = df_user_position.append(df)
            # 修改order status
            return "Success", df_user_position
        # 如果没成交
        else:
            # 修改order status
            return "Not Enough Cash", df_user_position

    def brokerResponseMarketOpen(self):
        """
        处理每天的开盘阶段.
        """
        # 获取三大表格, 当前持仓, 今日市场和pendingMarketOrder
        pendingMarketOrder = self.brokerdb.readMarketPendingOrder()
        # 如果pendingMarketOrder没有任何交易的话..直接退出函数
        if pendingMarketOrder.empty:
            return None
        userPosition = self.brokerdb.readCurrentPosition()
        # 获取可能要使用的股票池
        stock_pool_list = pendingMarketOrder['ts_code'].unique().tolist()
        stock_pool_price = self.marketdb.getMarketNow(
            ['ts_code', 'open'], {'ts_code': stock_pool_list})
        # 为这些表格set_index 便于查找
        stock_pool_price.set_index('ts_code', inplace=True)
        userPosition.set_index(['book', 'ts_code'], inplace=True)
        pendingMarketOrder.set_index('order_id', inplace=True)
        # 循环今天将要执行的Order!
        update_order_status_list = []
        for index, row in pendingMarketOrder.iterrows():
            message, userPosition = self.handleSingleMarketOrder(row['book'],
                                                                 row['ts_code'],
                                                                 row['amount'],
                                                                 row['amount_type'],
                                                                 stock_pool_price,
                                                                 userPosition,
                                                                 'open')
            update_order_status_list.append((message, index))
        # 即得到了需要更新到数据库的信息.
        # 更新order status
        self.brokerdb.updateOrderStatus(update_order_status_list)
        # 更新当前的仓位
        self.brokerdb.updateCurrentPosition(userPosition)

    def brokerResponseMarketMiddle(self):
        """
        处理市场的盘中阶段.
        """
        pass

    def brokerResponseMarketClose(self):
        """
        处理每天的开盘阶段.
        """
        # 获取三大表格, 当前持仓, 今日市场和pendingMarketOrder
        pendingMarketOrder = self.brokerdb.readMarketPendingOrder()
        # 如果pendingMarketOrder没有任何交易的话..直接退出函数
        if pendingMarketOrder.empty:
            return None
        userPosition = self.brokerdb.readCurrentPosition()
        # 获取可能要使用的股票池
        stock_pool_list = pendingMarketOrder['ts_code'].unique().tolist()
        stock_pool_price = self.marketdb.getMarketNow(
            ['ts_code', 'close'], {'ts_code': stock_pool_list})
        # 为这些表格set_index 便于查找
        stock_pool_price.set_index('ts_code', inplace=True)
        userPosition.set_index(['book', 'ts_code'], inplace=True)
        pendingMarketOrder.set_index('order_id', inplace=True)
        # 循环今天将要执行的Order!
        update_order_status_list = []
        for index, row in pendingMarketOrder.iterrows():
            message, userPosition = self.handleSingleMarketOrder(row['book'],
                                                                 row['ts_code'],
                                                                 row['amount'],
                                                                 row['amount_type'],
                                                                 stock_pool_price,
                                                                 userPosition,
                                                                 'close')
            update_order_status_list.append((message, index))
        # 即得到了需要更新到数据库的信息.
        # 更新order status
        self.brokerdb.updateOrderStatus(update_order_status_list)
        # 更新当前的仓位
        self.brokerdb.updateCurrentPosition(userPosition)

    def brokerFinishingToday(self):
        # 获取current position
        userPosition = self.brokerdb.readCurrentPosition()
        # 获取今天的行情数据
        stock_pool_price = self.marketdb.getMarketNow()
        # 创建只含有cash且价值为1的行
        temp_df = pd.DataFrame([['cash', 1]], columns=['ts_code', 'close'])
        # 和当天的行情数据合并
        stock_pool_price = stock_pool_price.append(temp_df)
        # 然后将持仓表格和股价数据表格merge一下用于向量计算
        calculation_df = pd.merge(
            userPosition, stock_pool_price, how='left', on='ts_code')
        # 计算当天的value, 如果当天没有价格, 则用前一天的价值代替.
        # 使用np.isnan考察今天的数据, 如果有空值, 则取原来的values, 否则取position * close的值.
        userPosition['value'] = np.where(np.isnan(calculation_df['close'].values), userPosition['value'].values, calculation_df['position'].values * \
            calculation_df['close'].values)
        userPosition['return'] = userPosition['value'].values - \
            userPosition['position'].values * userPosition['wavg_cost'].values
        userPosition['pct_return'] = np.where(userPosition['wavg_cost'].values == 0, 0, (
            userPosition['return'].values / np.abs(userPosition['position'].values * userPosition['wavg_cost'].values)) * 100)
        # 计算结束后, 将这个表格返回给数据库
        # userPosition 导入的时候是包含索引的, 运算过程中没有用到索引, 因此依然是有索引.
        self.brokerdb.updateCurrentPosition(userPosition, True)
        # 并将这个表格append回历史持仓数据库
        self.brokerdb.updateHistPositionCSV(userPosition)

    def brokerVectorResponseMarketClose(self):
        # 获取三大表格, 当前持仓, 今日市场和pendingMarketOrder.
        pendingMarketOrder = self.brokerdb.readMarketPendingOrder()
        # 如果pendingMarketOrder没有任何交易的话..直接退出函数.
        if pendingMarketOrder.empty:
            return None
        userPosition = self.brokerdb.readCurrentPosition()
        # 获取今日的marketnow.
        marketPrice = self.marketdb.getMarketNow()
        # 这里注意不要使用inplace = True的命名方法, 而是重新赋值给新的对象.
        daily_price = marketPrice.rename(columns={'close': 'price'})
        update_order_status_list, userPosition = self.vectorizedHandleMarketOrder(
            userPosition, daily_price, pendingMarketOrder)

        # 更新order status
        self.brokerdb.updateOrderStatus(update_order_status_list)
        # 更新当前的仓位
        self.brokerdb.updateCurrentPosition(userPosition)

    def vectorizedHandleMarketOrder(self, userPosition, daily_price, order_book):
        """
        向量化的处理市价单.
        userPosition 没有设置index的原生数据表.
        daily_price marketnow表格, 将要使用的一列价格为'price'
        order_book 原生的pending_orders Market

        """
        # 先合并价格和order_book
        order_book = pd.merge(order_book, daily_price,
                              how='left', on='ts_code')

        # 把value作为amount_type的统一转化为shares的数量.
        order_book['amount'] = np.where(order_book['amount_type'] == 'value', np.floor_divide(
            order_book['amount'], order_book['price']), order_book['amount'])

        # 计算order_amount向量. 此时的order_book['amount']全都是代表shares.
        # 相乘后得到不包含税费交易额
        order_amount = order_book['amount'].values * order_book['price'].values

        # 计算衍生出来的税费
        broker_fee = np.maximum(np.abs(order_amount) *
                                0.00012, np.full_like(order_amount, 5))
        broker_tax = np.abs(np.minimum(order_amount * 0.001,
                                       np.full_like(order_amount, 0)))
        total_transaction_cost = broker_fee + broker_tax

        # 计算总的payoff
        order_cost = order_amount + total_transaction_cost

        # 按照账户名称和order_cost排序
        order_book['order_cost'] = order_cost
        order_book = order_book.sort_values(by=['book', 'order_cost'])

        # 准备更新订单状态的序列.
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
            order_cost_cumsum = np.cumsum(
                this_book_order_book['order_cost'].values)
            # 假定用当前的现金按顺序累计执行, 会剩余多少钱?
            assume_order_complete = cash_available - order_cost_cumsum
            # 更新订单状态, 大于等于0的可以被成功执行, 否则会失败
            order_status_this_book = np.full(
                assume_order_complete.shape, 'pending')
            # 把没有今天价格的订单设置为-1
            assume_order_complete[np.isnan(assume_order_complete)] = -1
            order_status_this_book = np.where(
                assume_order_complete >= 0, 'Success', 'Not Enough Cash')
            # 对-1的值, 证明没有价格, 返回其他信息(这里是一个妥协)
            order_status_this_book[assume_order_complete == -
                                   1] = "No Price Available"
            # 计算剩余的现金
            # 再剩余的累加中, 寻找大于0的最小值. 也就是剩余的现金.
            cash_after = np.min(
                assume_order_complete[assume_order_complete >= 0])
            updated_order_status = np.append(
                updated_order_status, order_status_this_book)
            # 更新现金
            userPosition.loc[(each_book, 'cash'), 'position'] = cash_after

        # 把更新的订单状态赋值给order_book
        order_book['order_status'] = updated_order_status
        # 从而可以传出更新order_status的List of tuple
        order_status_tobereturned = order_book[[
            'order_status', 'order_id']].to_records(index=False).tolist()

        # 下面就是更复杂的更新仓位啦!
        # 用集合操作把没有建仓的账户股票组合找出来, 然后将表格append上去.
        order_book_index_set = set(order_book[order_book['order_status'] == 'Success'][[
                                   'book', 'ts_code']].to_records(index=False).tolist())
        position_index_set = set(userPosition.index.tolist())

        whatsnewposition = order_book_index_set.difference(position_index_set)

        # 如果这个集合不是空的, 说明userPosition需要加入新的行.
        if bool(whatsnewposition):
            index = pd.MultiIndex.from_tuples(list(whatsnewposition))
            append_df = pd.DataFrame(0, index, columns=userPosition.columns)
            userPosition = userPosition.append(append_df)

        # 合并userPosition和order_book.
        # 从orderbook中筛选已经成功的交易单, 以及有用的列
        temp_order_book = order_book[order_book['order_status'] == 'Success'][[
            'book', 'ts_code', 'amount', 'order_cost']]
        # 保证同一个book和同一个ts_code只有一个记录. (若存在相同账户对同一个证券的反复操作)
        temp_order_book.groupby(['book', 'ts_code']).sum()
        # 合并仓位表格和temp_order_book
        # 为了防止后续运算出错, 将缺失值替换为0.
        calculation_df = pd.merge(userPosition, temp_order_book, how='left', on=[
                                  'book', 'ts_code']).fillna(0)
        userPosition = userPosition.fillna(0)
        # 更新交易成功后的仓位
        position_after_trade = userPosition['position'].values + \
            calculation_df['amount'].values
        # 更新wavg_cost, 对于清仓后为0的部分, 成本变为0.
        userPosition['wavg_cost'] = np.where(position_after_trade == 0, 0, (userPosition['wavg_cost'].values *
                                                                            userPosition['position'].values + calculation_df['order_cost'].values) / position_after_trade)

        userPosition['position'] = userPosition['position'].values + \
            calculation_df['amount'].values
        return order_status_tobereturned, userPosition

    def addInvestorBooks(self, book_dict):
        """
        传入的类型是dictionary, 类似以下结构.
        {'yz' : {'cash' : 1000000 , 'commission' : 0.00012},
         'jx' : {'cash' : 2000000 , 'commission' : 0.00012}}
        """
        self.brokerdb.initialDepositCash(book_dict)
