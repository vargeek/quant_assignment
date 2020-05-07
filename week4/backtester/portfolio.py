from handler import Handler
from util import parse_symbol
import const
from const import OPEN, CLOSE, NONE, LONG, SHORT
from event import OrderEvent
import queue
from trade import Trade
import logging
from abc import abstractmethod

class Portfolio(Handler):
    @abstractmethod
    def force_close_open_trades(self):
        raise NotImplementedError("Should implement force_close_open_trades()!")
    @abstractmethod
    def get_all_trades(self):
        raise NotImplementedError("Should implement get_all_trades()!")

class BidAskPortfolio(Portfolio):
    def __init__(self, config, event_queue, data_handler, execution):
        super(BidAskPortfolio, self).__init__()

        self.__init_symbol_info(config)

        self.event_queue = event_queue
        self.data_handler = data_handler
        self.execution = execution

        # 状态
        self.current_bar = None
        self.open_trades = {}
        self.all_trades = []
        # `force_close_open_trades`所使用的最后一个bar
        self.pseudo_last_bar = None
    
    def __init_symbol_info(self, config):
        symbol = config.get('backtest', 'symbol')
        symbol = parse_symbol(symbol)
        self.commission_rate = const.COMMISSION_RATE_DICT[symbol]
        self.multiplier = const.MULTIPLIER_DICT[symbol]
        self.ticksize = const.TICKSIZE_DICT[symbol]

    def handle_bar(self, event):
        """
        更新`current_bar`, `pseudo_last_bar`  
        主力合约发生变化时，`force_close_open_trades`
        """
        if self.data_handler.len_latest_bars() > 1:
            self.current_bar = self.data_handler.get_latest_bars(n=1)
            self.pseudo_last_bar = self.current_bar
        else:
            # 刚开始回测或合约变化
            self.force_close_open_trades()

    def handle_signal(self, signal):
        if self.current_bar is not None:
            self._generate_order(signal, self.current_bar)

    def _generate_order(self, signal, bar):
        """
        if has current position:
            if direction unchanged: nothing to do,
            else: send an order to flat current trade
        else: no position, send order
        """

        if len(self.open_trades) > 0: # has current position
            open_trade = next(iter(self.open_trades.values()))
            if open_trade.direction != signal.direction: # direction changed
                # flat current trade
                if signal.direction == LONG:
                    price = bar.close_ask_price1
                else:
                    price = bar.close_bid_price1

                order = self._create_order_event(bar, signal, price, CLOSE, trade_id=open_trade.trade_id)
                self.event_queue.put(order)
        else: # no position
            if signal.direction == LONG:
                price = bar.close_ask_price1
            else:
                price = bar.close_bid_price1

            order = self._create_order_event(bar, signal, price, OPEN)
            self.event_queue.put(order)

    def _create_order_event(self, bar, signal, price, open_or_close, trade_id=None):
        return OrderEvent(
            symbol=bar.symbol,
            datetime=bar.datetime,
            price=price,
            quantity=1,
            direction=signal.direction,
            open_or_close=open_or_close,
            trade_id=trade_id,
        )

    def handle_fill(self, fill):
        if fill.open_or_close == OPEN: # open a new trade
            # if there is an open order in order_queue, cancel it first
            self.execution.cancel_open_orders()

            # create open trade
            open_trade = self._create_open_trade(fill)
            self.open_trades[open_trade.trade_id] = open_trade

        elif fill.open_or_close == CLOSE: # close open trade
            trade_id = fill.trade_id
            open_trade = self.open_trades.get(trade_id, None)
            if open_trade is None:
                logging.info(f"no trade found for trade_id: {trade_id}")
                return

            open_trade.exit_price = fill.price
            open_trade.exit_time = fill.datetime
            open_trade.profit = (open_trade.exit_price - open_trade.entry_price) * self.multiplier * open_trade.direction * open_trade.quantity

            # 取消和这个trade相关的所有order
            self.execution.cancel_orders_for_trade_id(trade_id)
            self.all_trades.append(open_trade)
            self.open_trades.pop(trade_id, None)

    def _create_open_trade(self, fill):
        trade = Trade(
            symbol=fill.symbol,
            trade_id=fill.trade_id,
            entry_time=fill.datetime,
            entry_price=fill.price,
            exit_time=None,
            exit_price=None,
            quantity=fill.quantity,
            direction=fill.direction,
            paper_pnl=None,
            profit=None
        )
        return trade

    def force_close_open_trades(self):
        if len(self.open_trades) == 0:
            return

        logging.info(f"There are {len(self.open_trades)} open trade(s) left")

        bar = self.pseudo_last_bar
        if bar is None:
            bar = self.data_handler.get_latest_bars(n=1)

        assert bar is not None, "bar不应为None"
        
        for trade_id in list(self.open_trades): # list(): copy keys
            open_trade = self.open_trades[trade_id]
            if open_trade.direction == LONG:
                open_trade.exit_price = bar.close_bid_price1
            else:
                open_trade.exit_price = bar.close_ask_price1

            open_trade.exit_time = bar.datetime
            open_trade.profit = (open_trade.exit_price - open_trade.entry_price) * self.multiplier * open_trade.direction * open_trade.quantity
            self.all_trades.append(open_trade)
            self.open_trades.pop(trade_id, None)

    def get_all_trades(self):
        return self.all_trades


class ExcelPortfolio(Portfolio):
    """
    模拟第三周excel版本
    """
    def __init__(self, config, event_queue, data_handler, execution):
        super(ExcelPortfolio, self).__init__()
        self.__init_symbol_info(config)

        self.event_queue = event_queue
        self.data_handler = data_handler
        self.execution = execution

        # 状态
        self.current_bar = None
        self.open_trade = None
        self.all_trades = []
        # `force_close_open_trades`所使用的最后一个bar
        self.pseudo_last_bar = None

    def __init_symbol_info(self, config):
        symbol = config.get('backtest', 'symbol')
        symbol = parse_symbol(symbol)
        self.commission_rate = 0
        self.multiplier = 10
        self.ticksize = 2
        

    def handle_bar(self, event):
        if self.data_handler.len_latest_bars() > 1:
            self.current_bar = self.data_handler.get_latest_bars(n=1)
            self.pseudo_last_bar = self.current_bar
        else:
            # 刚开始回测或合约变化
            self.force_close_open_trades()

    def force_close_open_trades(self):
        if self.open_trade is None:
            return

        bar = self.pseudo_last_bar
        if bar is None:
            bar = self.data_handler.get_latest_bars(n=1)
        assert bar is not None, "bar不应为None"
        
        open_trade = self.open_trade
        self.all_trades.append(open_trade)
        self.open_trade = None

    def handle_signal(self, signal):
        current_bar = self.current_bar
        if current_bar is None:
            return
    
        self._generate_order(signal, current_bar)
            

    def _generate_order(self, signal, bar):
        price = bar.close
        if self.open_trade is not None:
            open_trade = self.open_trade

            if open_trade.direction != signal.direction:
                # flat
                order = self._create_order_event(bar, signal, price, CLOSE, trade_id=open_trade.trade_id)
                self.event_queue.put(order)

                # open
                order = self._create_order_event(bar, signal, price, OPEN)
                self.event_queue.put(order)
        else:
            # open
            order = self._create_order_event(bar, signal, price, OPEN)
            self.event_queue.put(order)

    def _create_order_event(self, bar, signal, price, open_or_close, trade_id=None):
        return OrderEvent(
            symbol=bar.symbol,
            datetime=bar.datetime,
            price=price,
            quantity=1,
            direction=signal.direction,
            open_or_close=open_or_close,
            trade_id=trade_id,
        )

    def handle_fill(self, fill):
        if fill.open_or_close == OPEN: # open a new trade
            # create open trade
            open_trade = self._create_open_trade(fill)
            self.open_trade = open_trade
        elif fill.open_or_close == CLOSE: # close open trade
            trade_id = fill.trade_id
            open_trade = self.open_trade
            if open_trade is not None and open_trade.trade_id == fill.trade_id:
                open_trade.exit_price = fill.price
                open_trade.exit_time = fill.datetime
                open_trade.profit = (open_trade.exit_price - open_trade.entry_price) * self.multiplier * open_trade.direction
                # open_trade.paper_pnl = 
                # 取消和这个trade相关的所有order
                self.execution.cancel_orders_for_trade_id(trade_id)
                self.all_trades.append(open_trade)
                self.open_trade = None

    def _create_open_trade(self, fill):
        trade = Trade(
            symbol=fill.symbol,
            trade_id=fill.trade_id,
            entry_time=fill.datetime,
            entry_price=fill.price,
            exit_time=None,
            exit_price=None,
            quantity=fill.quantity,
            direction=fill.direction,
            paper_pnl=None,
            profit=None
        )
        return trade

    def get_all_trades(self):
        return self.all_trades