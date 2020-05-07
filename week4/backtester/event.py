import shortuuid
from const import BAR, SIGNAL, ORDER, FILL

class Event:
    __repr_attrs__ = []

    def __repr__(self):
        attrs = self.__class__.__repr_attrs__
        return str({attr: getattr(self, attr)for attr in attrs if hasattr(self, attr) })

class Bar(Event):
    __slots__ = [
        'type',
        'symbol',
        'datetime',
        'high',
        'open',
        'low',
        'close',
        'high_ask_price1',
        'open_ask_price1',
        'low_ask_price1',
        'close_ask_price1',
        'high_bid_price1',
        'open_bid_price1',
        'low_bid_price1',
        'close_bid_price1',
        'volume',
        'open_ask_volume1',
        'close_ask_volume1',
        'open_bid_volume1',
        'close_bid_volume1',
    ]
    __repr_attrs__ = ['type', 'symbol', 'datetime']

    def __init__(self, symbol, datetime, high, open, low, close, high_ask_price1, open_ask_price1, low_ask_price1, close_ask_price1, high_bid_price1, open_bid_price1, low_bid_price1, close_bid_price1, volume, open_ask_volume1, close_ask_volume1, open_bid_volume1, close_bid_volume1):
        super(Bar, self).__init__()

        self.type = BAR
        self.symbol = symbol
        self.datetime = datetime
        self.high = high
        self.open = open
        self.low = low
        self.close = close
        self.high_ask_price1 = high_ask_price1
        self.open_ask_price1 = open_ask_price1
        self.low_ask_price1 = low_ask_price1
        self.close_ask_price1 = close_ask_price1
        self.high_bid_price1 = high_bid_price1
        self.open_bid_price1 = open_bid_price1
        self.low_bid_price1 = low_bid_price1
        self.close_bid_price1 = close_bid_price1
        self.volume = volume
        self.open_ask_volume1 = open_ask_volume1
        self.close_ask_volume1 = close_ask_volume1
        self.open_bid_volume1 = open_bid_volume1
        self.close_bid_volume1 = close_bid_volume1

class SignalEvent(Event):
    __slots__ = [
        'type',
        'symbol',
        'datetime',
        'direction',
        'strength',
        'strategy_id',
    ]
    __repr_attrs__ = [
        'type',
        'symbol',
        'datetime',
        'direction',
        'strength'
    ]
    def __init__(self, symbol, datetime, direction, strength, strategy_id):
        """
        初始化  
        direction: 信号方向  
        strength: 信号强度  
        strategy_id: 策略id  
        """
        super(SignalEvent, self).__init__()

        self.type = SIGNAL
        self.symbol = symbol
        self.datetime = datetime
        self.direction = direction
        self.strength = strength
        self.strategy_id = strategy_id


class OrderEvent(Event):
    __slots__ = [
        'type',
        'symbol',
        'datetime',
        'price',
        'quantity',
        'direction',
        'open_or_close',
        'trade_id',
    ]
    __repr_attrs__ = [
        'type',
        'symbol',
        'datetime',
        'price',
        'quantity',
        'direction',
    ]

    def __init__(self, symbol, datetime, price, quantity, direction, open_or_close, trade_id=None):
        """
        初始化  
        direction: LONG | SHORT
        """
        super(OrderEvent, self).__init__()
        self.type = ORDER
        self.symbol = symbol
        self.datetime = datetime
        self.price = price
        self.quantity = quantity
        self.direction = direction
        self.open_or_close = open_or_close
        self.trade_id = shortuuid.uuid() if trade_id is None else trade_id

class FillEvent(Event):
    """
    成交事件
    """
    __slots__ = [
        'type',
        'symbol',
        'datetime',
        'price',
        'quantity',
        'direction',
        'open_or_close',
        'trade_id',
    ]

    __repr_attrs__ = [
        'type',
        'symbol',
        'datetime',
        'price',
        'quantity',
        'direction',
        'open_or_close',
    ]

    def __init__(self, symbol, datetime, price, quantity, direction, open_or_close, trade_id):
        super(FillEvent, self).__init__()
        self.type = FILL
        self.symbol = symbol
        self.datetime = datetime
        self.price = price
        self.quantity = quantity
        self.direction = direction
        self.open_or_close = open_or_close
        self.trade_id = trade_id
