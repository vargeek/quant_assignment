from handler import Handler
import queue
from const import LONG, SHORT, OPEN, CLOSE
from event import FillEvent
from abc import abstractmethod

class Execution(Handler):
    @abstractmethod
    def cancel_open_orders(self):
        raise NotImplementedError("Should implement cancel_open_orders()!")
    @abstractmethod
    def cancel_all_orders(self):
        raise NotImplementedError("Should implement cancel_all_orders()!")
    @abstractmethod
    def cancel_orders_for_trade_id(self, trade_id):
        raise NotImplementedError("Should implement cancel_orders_for_trade_id()!")



class SimExecutionHandler(Execution):
    def __init__(self, config, event_queue, data_handler):
        super(SimExecutionHandler, self).__init__()

        self.event_queue = event_queue
        self.data_handler = data_handler

        self.order_queue = queue.Queue()

    def handle_bar(self, event):
        """
        cross order in order_queue
        """
        bars = self.data_handler.get_latest_bars(n=2)
        if len(bars) < 2: # 刚开始回测或合约变化
            return 
        
        last_bar, current_bar = bars[0], bars[1]
            # self.pseudo_last_bar = current_bar
        incomplete_orders = queue.Queue()
        while not self.order_queue.empty():
            order = self.order_queue.get()
            fill = self._cross(order, last_bar, current_bar)
            if fill is None:
                incomplete_orders.put(order)
            else:
                self.event_queue.put(fill)

        while not incomplete_orders.empty():
            self.order_queue.put(incomplete_orders.get())

    def _cross(self, order, last_bar, curr_bar):
        traded = False
        if order.direction == LONG:
            if order.open_or_close == OPEN:
                if order.price >= curr_bar.low_ask_price1 and curr_bar.low_ask_price1 > 0 and order.price < last_bar.close_ask_price1:
                    # cannot buy at limit up
                    # 下降趋势
                    traded = True
            elif order.open_or_close == CLOSE:
                if order.price >= curr_bar.low_ask_price1 and order.price <= curr_bar.high_ask_price1:
                    traded = True
        elif order.direction == SHORT:
            if order.open_or_close == OPEN:
                if order.price <= curr_bar.high_bid_price1 and order.price > last_bar.close_bid_price1:
                    # 上升趋势
                    traded = True
            elif order.open_or_close == CLOSE:
                if order.price >= curr_bar.low_bid_price1 and order.price <= curr_bar.high_bid_price1:
                    traded = True

        if traded:
            return FillEvent(
                symbol=order.symbol,
                datetime=curr_bar.datetime,
                price=order.price,
                quantity=order.quantity,
                direction=order.direction,
                open_or_close=order.open_or_close,
                trade_id=order.trade_id,
            )

        return None

    def handle_order(self, event):
        # 放入`order_queue`，下一次`handle_bar`撮合
        self.order_queue.put(event)

    def cancel_open_orders(self):
        close_orders = queue.Queue()
        while not self.order_queue.empty():
            order = self.order_queue.get()
            if order.open_or_close == CLOSE:
                close_orders.put(order)

        while not close_orders.empty():
            self.order_queue.put(close_orders.get())

    def cancel_all_orders(self):
        while not self.order_queue.empty():
            self.order_queue.get()

    def cancel_orders_for_trade_id(self, trade_id):
        if trade_id is None:
            return

        keep_orders = queue.Queue()
        while not self.order_queue.empty():
            order = self.order_queue.get()
            if order.trade_id != trade_id:
                keep_orders.put(order)

        while not keep_orders.empty():
            self.order_queue.put(keep_orders.get())


class ExcelExecution(Execution):
    """
    模拟第三周excel版本
    """
    def __init__(self, config, event_queue, data_handler):
        super(ExcelExecution, self).__init__()

        self.event_queue = event_queue
        self.data_handler = data_handler

    def handle_bar(self, event):
        pass

    def handle_order(self, order):
        bars = self.data_handler.get_latest_bars(n=2)
        if len(bars) < 2: # 刚开始回测或合约变化
            return 
        
        last_bar, current_bar = bars[0], bars[1]
        fill = self._cross(order, last_bar, current_bar)
        self.event_queue.put(fill)

    def _cross(self, order, last_bar, curr_bar):
        return FillEvent(
            symbol=order.symbol,
            datetime=curr_bar.datetime,
            price=order.price,
            quantity=order.quantity,
            direction=order.direction,
            open_or_close=order.open_or_close,
            trade_id=order.trade_id,
        )
    def cancel_open_orders(self):
        pass

    def cancel_all_orders(self):
        pass

    def cancel_orders_for_trade_id(self, trade_id):
        pass
