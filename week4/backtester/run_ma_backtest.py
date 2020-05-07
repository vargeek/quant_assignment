from backtest import BackTest
from configparser import ConfigParser
from datahandler import FileMDEngine
from strategy import MovingAverageCrossStrategy
from portfolio import BidAskPortfolio
from execution import SimExecutionHandler
from performance import PerformanceMetric


if __name__ == "__main__":
    config = ConfigParser()
    config.read('./config/config.conf')

    def create_handlers(config, event_queue):
        """
        create data_handler, strategy, portfolio, execution
        """
        data_handler = FileMDEngine(config, event_queue)
        strategy = MovingAverageCrossStrategy(config, event_queue, data_handler)
        execution = SimExecutionHandler(config, event_queue, data_handler)
        portfolio = BidAskPortfolio(config, event_queue, data_handler, execution)

        return data_handler, strategy, portfolio, execution

    test = BackTest(config, create_handlers)
    test.run_backtest()
    
    metric = PerformanceMetric(test, config)
    metrics = metric.calculate_performance()
    print(metrics['data'])
    print(metrics['trades_df'])