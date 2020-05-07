from abc import ABC, abstractmethod
import pandas as pd
from event import Bar
from collections import deque
from itertools import islice

class MDEngine(ABC):
    """
    Abstract class
    """
    @abstractmethod
    def get_latest_bars(self, n=1):
        """
        获取最近n根bar，如果可用数不足n，则返回所有bar。
        """
        raise NotImplementedError("Should implement get_latest_bars()!")

    @abstractmethod
    def len_latest_bars(self):
        """
        获取最近bars个数
        """
        raise NotImplementedError("Should implement len_latest_bars()!")

    @abstractmethod
    def publish_md(self):
        """
        发布bar事件
        """
        raise NotImplementedError("Should implement publish_md()！")

    @abstractmethod
    def get_dataframe(self):
        """
        获取原始DataFrame数据
        """
        raise NotImplementedError("Should implement get_dataframe()！")

class FileMDEngine(MDEngine):
    def __init__(self, config, event_queue):
        datapath = config.get('FileMDEngine', 'datapath')

        self.event_queue = event_queue

        self.datapath = datapath
        self.latest_bars = deque()

        self.data = self.load_dataframe()
        self.df_rows = self.data.iterrows()

    def load_dataframe(self):
        df = pd.read_csv(self.datapath)
        columns = ['symbol', 'datetime', 'high', 'open', 'low', 'close', 'high_ask_price1', 'open_ask_price1', 'low_ask_price1', 'close_ask_price1', 'high_bid_price1', 'open_bid_price1', 'low_bid_price1', 'close_bid_price1', 'volume', 'open_ask_volume1', 'close_ask_volume1', 'open_bid_volume1', 'close_bid_volume1']
        df = df[columns]
        df.datetime = pd.to_datetime(df.datetime)
        df.index = df.datetime
        return df

    def get_dataframe(self):
        """
        获取原始DataFrame数据
        """
        return self.data

    def get_latest_bars(self, n=1):
        len_bars = len(self.latest_bars)
        if self.latest_bars is None or len_bars == 0:
            return None

        if n == 1:
            return self.latest_bars[-1]
        else:
            start = max(len_bars-n, 0)
            return list(islice(self.latest_bars, start, len_bars))

    def len_latest_bars(self):
        return len(self.latest_bars)
        
    def publish_md(self):
        """
        发布一个bar事件
        """
        try:
            last_bar = self.get_latest_bars(n=1)
            _, bar_data = next(self.df_rows)
            bar = self._create_bar_event(bar_data)
            if last_bar is None or bar.symbol != last_bar.symbol:
                # 刚开始回测或合约发生变化
                self.latest_bars = deque(maxlen=2400)

            self.latest_bars.append(bar)
        except StopIteration:
            return False
        else:
            self.event_queue.put(bar)

        return True

    def _create_bar_event(self, data):
        return Bar(
            symbol = data.symbol,
            datetime = data.datetime,
            high = data.high,
            open = data.open,
            low = data.low,
            close = data.close,
            high_ask_price1 = data.high_ask_price1,
            open_ask_price1 = data.open_ask_price1,
            low_ask_price1 = data.low_ask_price1,
            close_ask_price1 = data.close_ask_price1,
            high_bid_price1 = data.high_bid_price1,
            open_bid_price1 = data.open_bid_price1,
            low_bid_price1 = data.low_bid_price1,
            close_bid_price1 = data.close_bid_price1,
            volume = data.volume,
            open_ask_volume1 = data.open_ask_volume1,
            close_ask_volume1 = data.close_ask_volume1,
            open_bid_volume1 = data.open_bid_volume1,
            close_bid_volume1 = data.close_bid_volume1,
        )