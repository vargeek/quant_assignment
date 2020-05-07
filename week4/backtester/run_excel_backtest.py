from backtest import BackTest
from configparser import ConfigParser
from datahandler import FileMDEngine
from strategy import ExcelStrategy
from portfolio import ExcelPortfolio
from execution import ExcelExecution
from performance import PerformanceMetric
import pandas as pd


def load_excel_result():
    df2 = pd.read_csv('data/IF2004_20200417Backtester.CSV').set_index('datetime')
    df2.index = pd.to_datetime(df2.index)
    df2 = df2[['close', 'Position', 'TradeP&L', 'CumP&L']]
    return df2

if __name__ == "__main__":
    # 模拟excel版回测
    config = ConfigParser()
    config.read('./config/config-excel.conf')

    def create_handlers(config, event_queue):
        """
        create data_handler, strategy, portfolio, execution
        """
        data_handler = FileMDEngine(config, event_queue)
        strategy = ExcelStrategy(config, event_queue, data_handler)
        execution = ExcelExecution(config, event_queue, data_handler)
        portfolio = ExcelPortfolio(config, event_queue, data_handler, execution)

        return data_handler, strategy, portfolio, execution

    test = BackTest(config, create_handlers)
    test.run_backtest()

    metric = PerformanceMetric(test, config)
    metric.multiplier = 10
    metrics = metric.calculate_performance()

    df1 = metrics.get('data')

    columns = ['close', 'position', 'tradepnl_wo_commission', 'cumpnl_wo_commission']
    df1 = df1[columns]

    df2 = load_excel_result()
    df2.columns = columns

    precision=9
    # print(list(zip(df1['cumpnl_wo_commission'], df2['cumpnl_wo_commission'])))
    cmp_result = (df1.isna() & df2.isna()) | ((df1 - df2).abs().round(precision) == 0)
    print('all true: ', cmp_result.all().all())
    cmp_result.describe()
