import const
import pandas as pd

class PerformanceMetric:
    def __init__(self, test, config):
        symbol = config.get('backtest', 'symbol')
        initial_capital = int(config.get('backtest', 'initial_capital'))   
        data = test.data_handler.get_dataframe()
        trades = test.portfolio.get_all_trades()

        self.multiplier = const.MULTIPLIER_DICT[symbol]
        self.commission_rate = const.COMMISSION_RATE_DICT[symbol]
        self.initial_capital = initial_capital
        self.data = data
        self.trades = trades
    
    def load_trade(self):
        data = self.data
        data['trade'] = 0
        data['tradeprice'] = 0
        for trade in self.trades:
            data.loc[trade.entry_time, 'trade'] += trade.direction * trade.quantity
            data.loc[trade.entry_time, 'tradeprice'] = trade.entry_price
            if trade.exit_time is not None:
                data.loc[trade.exit_time, 'trade'] -= trade.direction * trade.quantity
                data.loc[trade.exit_time, 'tradeprice'] = trade.exit_price

        data['position'] = data.trade.cumsum()
        data['tradepnl'] = self.multiplier * data.trade * (data.close.shift() - data.tradeprice) - self.commission_rate * data.tradeprice * abs(data.trade)
        
        data['pospnl'] = self.multiplier * data.position * (data.close - data.close.shift()).fillna(0)
        data['barpnl'] = data.pospnl + data.tradepnl
        data['cumpnl'] = data.barpnl.cumsum()
        data['tradepnl_wo_commission'] = self.multiplier * data.trade * (data.close.shift() - data.tradeprice).fillna(0)
        data['barpnl_wo_commission'] = data.pospnl + data.tradepnl_wo_commission
        data['cumpnl_wo_commission'] = data.barpnl_wo_commission.cumsum()
        
        trades_df = pd.DataFrame([trade.to_dict() for trade in self.trades]).set_index('trade_id')

        return data, trades_df

    def calculate_performance(self):
        data, trades_df = self.load_trade()
        # TODO: calc metrics
        return {
            'data': data,
            'trades_df': trades_df,
        }




    # def calculate_performance(self):
    #     all_trades = self.portfolio.get_all_trades()
    #     if all_trades is None or len(all_trades) == 0:
    #         logging.warn("No trade, no P&L")
    #         return

    #     metric = PerformanceMetric(self.symbol, self.initial_capital, self.data_handler.get_dataframe(), all_trades)

    #     metrics = metric.calculate_performance()
    #     return metrics

    # def show_performance(self):
    #     # show
    #     pass
