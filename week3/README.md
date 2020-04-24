# week3

1. [x] 在Excel中使用自己合成的数据测试简单的交易策略  
   [IF2004_20200417Backtester.xlsx](data/IF2004_20200417Backtester.xlsx)

2. [x] 完成Lecture3.ipynb中的python策略部分，确保和Excel中的计算结果一致  
   [Lecture3.ipynb](Lecture3.ipynb)
3. [x] 封装以上的过程，完成BackTest类，使得可以方便的测试多个简单策略，完成NaiveMA类  
   [Lecture3.ipynb](Lecture3.ipynb)
4. [x] 阅读backtester中的代码，理解回测各个模块的作用
   - backtest
     - 执行回测，运行整个模块的事件循环
     - 显示测试结果
   - datahandler：
     - 从数据源获取数据，将bar数据事件发布到事件队列。
     - 为各个模块提供历史数据。
   - event：bar、信号等各类事件
   - strategy：接收bar事件，按照一定策略产生信号事件。
   - portfolio：接收信号事件和成交回报事件，产生订单事件。
     - 根据信号事件产生订单事件
     - 根据成交回报事件更新相关数据
   - execution：接收订单事件，模拟交易所的撮合过程，产生成交回报事件。
