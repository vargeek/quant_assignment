from event import SignalEvent
from handler import Handler
import shortuuid
from const import NONE, LONG, SHORT
import numpy as np
import logging

class Strategy(Handler):
    pass

class MovingAverageCrossStrategy(Strategy):
    """
    移动双均线策略
    """

    def __init__(self, config, event_queue, data_handler):
        short_window = int(config.get('MovingAverageCross', 'short_window'))
        long_window = int(config.get('MovingAverageCross', 'long_window'))

        self.event_queue = event_queue
        self.data_handler = data_handler
        self.short_window = short_window
        self.long_window = long_window
        self.strategy_id = shortuuid.uuid()
        
        # 状态
        # 方向： LONG|SHORT
        self.direction = NONE

    def handle_bar(self, event):
        if self.data_handler.len_latest_bars() >= self.long_window:
            bars = self.data_handler.get_latest_bars(n=self.long_window)
            asks = np.array([bar.close_ask_price1 for bar in bars])
            bids = np.array([bar.close_bid_price1 for bar in bars])
            long_window_avg = np.average((asks+bids)*0.5)
            short_window_avg = np.average((asks[-self.short_window:]+bids[-self.short_window:])*0.5)

            direction = NONE
            if long_window_avg > short_window_avg + 1:
                direction = LONG
            elif long_window_avg < short_window_avg - 1:
                direction = SHORT

            if direction != NONE and self.direction != direction:
                self.direction = direction
                signal = self._create_signal_event(bars[-1], direction)
                self.event_queue.put(signal)

    def _create_signal_event(self, bar, direction, strength = 0):
        return SignalEvent(
            symbol=bar.symbol,
            datetime=bar.datetime,
            direction=direction,
            strength=strength,
            strategy_id=self.strategy_id,
        )


class ExcelStrategy(Strategy):
    """
    模拟第三周excel版本
    """
    def __init__(self, config, event_queue, data_handler):
        super(ExcelStrategy, self).__init__()

        short_window = int(config.get('ExcelStrategy', 'short_window'))
        long_window = int(config.get('ExcelStrategy', 'long_window'))

        self.event_queue = event_queue
        self.data_handler = data_handler
        self.short_window = short_window
        self.long_window = long_window
        self.strategy_id = shortuuid.uuid()
        
        # 状态
        # 方向： LONG|SHORT
        self.direction = NONE

    def handle_bar(self, event):
        if self.data_handler.len_latest_bars() >= self.long_window:
            bars = self.data_handler.get_latest_bars(n=self.long_window)
            close = np.array([bar.close for bar in bars])
            long_window_avg = np.average(close)
            short_window_avg = np.average(close[-self.short_window:])

            direction = LONG if short_window_avg >= long_window_avg else SHORT

            if self.direction != direction:
                self.direction = direction
                signal = self._create_signal_event(bars[-1], direction)
                self.event_queue.put(signal)

    def _create_signal_event(self, bar, direction, strength = 0):
        return SignalEvent(
            symbol=bar.symbol,
            datetime=bar.datetime,
            direction=direction,
            strength=strength,
            strategy_id=self.strategy_id,
        )
