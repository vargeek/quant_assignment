class Trade:
    __slots__ = [
        'symbol',
        'trade_id',
        'entry_time',
        'entry_price',
        'exit_time',
        'exit_price',
        'quantity',
        'direction',
        'paper_pnl',
        'profit',
        # 'stoploss_price',
        # 'profit_target_price',
    ]

    def __init__(self, symbol, trade_id, entry_time, entry_price, exit_time, exit_price, quantity, direction, paper_pnl, profit):
        self.symbol = symbol
        self.trade_id = trade_id
        self.entry_time = entry_time
        self.entry_price = entry_price
        self.exit_time = exit_time
        self.exit_price = exit_price
        self.quantity = quantity
        self.direction = direction
        self.paper_pnl = paper_pnl
        self.profit = profit


    def to_dict(self):
        return {
            'symbol': self.symbol,
            'trade_id': self.trade_id,
            'entry_time': self.entry_time,
            'entry_price': self.entry_price,
            'exit_time': self.exit_time,
            'exit_price': self.exit_price,
            'quantity': self.quantity,
            'direction': self.direction,
            'paper_pnl': self.paper_pnl,
            'profit': self.profit,
        }