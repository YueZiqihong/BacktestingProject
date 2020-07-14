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
        try:
            stock_price = df_stock_price.loc[ts_code, marketPhase]
        except KeyError:
            return "No Price Available", df_user_position

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
        if_deal_finish = df_user_position.loc[(
            book, 'cash'), 'position'] - deal_cost
        if if_deal_finish >= 0:
            df_user_position.loc[(book, 'cash'), 'position'] = if_deal_finish
            if (book, ts_code) in df_user_position.index:
                if df_user_position.loc[(book, ts_code), 'position'] + deal_shares != 0:
                    df_user_position.loc[(book, ts_code), 'wavg_cost'] = (df_user_position.loc[(book, ts_code), 'wavg_cost'] * df_user_position.loc[(
                        book, ts_code), 'position'] + deal_cost) / (df_user_position.loc[(book, ts_code), 'position'] + deal_shares)
                else:
                    df_user_position.loc[(book, ts_code), 'wavg_cost'] = 0
                    pass
                df_user_position.loc[(book, ts_code),
                                     'position'] += deal_shares
            else:
                df = pd.DataFrame([[deal_shares, None, deal_cost / deal_shares, None, None]], columns=[
                                  'position', 'value', 'wavg_cost', 'return', 'pct_return'], index=[(book, ts_code)])
                df_user_position = df_user_position.append(df)
            return "Success", df_user_position
        else:
            return "Not Enough Cash", df_user_position

    def brokerResponseMarketOpen(self):
        pendingMarketOrder = self.brokerdb.readMarketPendingOrder()
        if pendingMarketOrder.empty:
            return None
        userPosition = self.brokerdb.readCurrentPosition()
        stock_pool_list = pendingMarketOrder['ts_code'].unique().tolist()
        stock_pool_price = self.marketdb.getMarketNow(
            ['ts_code', 'open'], {'ts_code': stock_pool_list})
        stock_pool_price.set_index('ts_code', inplace=True)
        userPosition.set_index(['book', 'ts_code'], inplace=True)
        pendingMarketOrder.set_index('order_id', inplace=True)
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
        self.brokerdb.updateOrderStatus(update_order_status_list)
        self.brokerdb.updateCurrentPosition(userPosition)

    def brokerResponseMarketMiddle(self):
        pass

    def brokerResponseMarketClose(self):
        pendingMarketOrder = self.brokerdb.readMarketPendingOrder()
        if pendingMarketOrder.empty:
            return None
        userPosition = self.brokerdb.readCurrentPosition()
        stock_pool_list = pendingMarketOrder['ts_code'].unique().tolist()
        stock_pool_price = self.marketdb.getMarketNow(
            ['ts_code', 'close'], {'ts_code': stock_pool_list})
        stock_pool_price.set_index('ts_code', inplace=True)
        userPosition.set_index(['book', 'ts_code'], inplace=True)
        pendingMarketOrder.set_index('order_id', inplace=True)
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
        self.brokerdb.updateOrderStatus(update_order_status_list)
        self.brokerdb.updateCurrentPosition(userPosition)

    def brokerFinishingToday(self):
        userPosition = self.brokerdb.readCurrentPosition()
        stock_pool_price = self.marketdb.getMarketNow()
        temp_df = pd.DataFrame([['cash', 1]], columns=['ts_code', 'close'])
        stock_pool_price = stock_pool_price.append(temp_df)
        calculation_df = pd.merge(
            userPosition, stock_pool_price, how='left', on='ts_code')
        userPosition['value'] = np.where(np.isnan(calculation_df['close'].values), userPosition['value'].values, calculation_df['position'].values * \
            calculation_df['close'].values)
        userPosition['return'] = userPosition['value'].values - \
            userPosition['position'].values * userPosition['wavg_cost'].values
        userPosition['pct_return'] = np.where(userPosition['wavg_cost'].values == 0, 0, (
            userPosition['return'].values / np.abs(userPosition['position'].values * userPosition['wavg_cost'].values)) * 100)
        self.brokerdb.updateCurrentPosition(userPosition, True)
        self.brokerdb.updateHistPositionCSV(userPosition)

    def brokerVectorResponseMarketClose(self):
        pendingMarketOrder = self.brokerdb.readMarketPendingOrder()
        if pendingMarketOrder.empty:
            return None
        userPosition = self.brokerdb.readCurrentPosition()
        marketPrice = self.marketdb.getMarketNow()
        daily_price = marketPrice.rename(columns={'close': 'price'})
        update_order_status_list, userPosition = self.vectorizedHandleMarketOrder(
            userPosition, daily_price, pendingMarketOrder)
        self.brokerdb.updateOrderStatus(update_order_status_list)
        self.brokerdb.updateCurrentPosition(userPosition)

    def vectorizedHandleMarketOrder(self, userPosition, daily_price, order_book):
        order_book = pd.merge(order_book, daily_price,
                              how='left', on='ts_code')
        order_book['amount'] = np.where(order_book['amount_type'] == 'value', np.floor_divide(
            order_book['amount'], order_book['price']), order_book['amount'])
        order_amount = order_book['amount'].values * order_book['price'].values

        broker_fee = np.maximum(np.abs(order_amount) *
                                0.00012, np.full_like(order_amount, 5))
        broker_tax = np.abs(np.minimum(order_amount * 0.001,
                                       np.full_like(order_amount, 0)))
        total_transaction_cost = broker_fee + broker_tax
        order_cost = order_amount + total_transaction_cost
        order_book['order_cost'] = order_cost
        order_book = order_book.sort_values(by=['book', 'order_cost'])
        updated_order_status = np.array([])

        for each_book in np.unique(order_book['book'].values):
            this_book_order_book = order_book[order_book['book'] == each_book]
            if this_book_order_book.empty:
                continue
            cash_available = userPosition.loc[(each_book, 'cash'), 'position']
            order_cost_cumsum = np.cumsum(
                this_book_order_book['order_cost'].values)
            assume_order_complete = cash_available - order_cost_cumsum
            order_status_this_book = np.full(
                assume_order_complete.shape, 'pending')
            assume_order_complete[np.isnan(assume_order_complete)] = -1
            order_status_this_book = np.where(
                assume_order_complete >= 0, 'Success', 'Not Enough Cash')
            order_status_this_book[assume_order_complete == -
                                   1] = "No Price Available"
            cash_after = np.min(
                assume_order_complete[assume_order_complete >= 0])
            updated_order_status = np.append(
                updated_order_status, order_status_this_book)
            userPosition.loc[(each_book, 'cash'), 'position'] = cash_after
        order_book['order_status'] = updated_order_status
        order_status_tobereturned = order_book[[
            'order_status', 'order_id']].to_records(index=False).tolist()

        order_book_index_set = set(order_book[order_book['order_status'] == 'Success'][[
                                   'book', 'ts_code']].to_records(index=False).tolist())
        position_index_set = set(userPosition.index.tolist())
        whatsnewposition = order_book_index_set.difference(position_index_set)

        if bool(whatsnewposition):
            index = pd.MultiIndex.from_tuples(list(whatsnewposition))
            append_df = pd.DataFrame(0, index, columns=userPosition.columns)
            userPosition = userPosition.append(append_df)

        temp_order_book = order_book[order_book['order_status'] == 'Success'][[
            'book', 'ts_code', 'amount', 'order_cost']]
        temp_order_book.groupby(['book', 'ts_code']).sum()
        calculation_df = pd.merge(userPosition, temp_order_book, how='left', on=[
                                  'book', 'ts_code']).fillna(0)
        userPosition = userPosition.fillna(0)
        position_after_trade = userPosition['position'].values + \
            calculation_df['amount'].values
        userPosition['wavg_cost'] = np.where(position_after_trade == 0, 0, (userPosition['wavg_cost'].values *
                                                                            userPosition['position'].values + calculation_df['order_cost'].values) / position_after_trade)

        userPosition['position'] = userPosition['position'].values + \
            calculation_df['amount'].values
        return order_status_tobereturned, userPosition

    def addInvestorBooks(self, book_dict):
        self.brokerdb.initialDepositCash(book_dict)
