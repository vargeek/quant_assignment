# %%
import pandas as pd
import datetime
import functools

# %%
def get_trade_time():
    """ 
    Return trade datettime
    """
    morning_trade_start_datetime = '09:30:00'
    morning_trade_end_datetime = '11:30:00'
    afternoon_trade_start_datetime = '13:00:00'
    afternoon_trade_end_datetime = '15:30:00'
    
    return (morning_trade_start_datetime, morning_trade_end_datetime, afternoon_trade_start_datetime,
    afternoon_trade_end_datetime)

def raw2tick(df):
    """
    处理原始数据：  
    - 同1秒只出现一次的数据，当成第0.5s数据处理
    - 交易时间过滤
    """

    # `Time`与下一个tick数据不同，则为第0.5s数据
    # 同1秒有两条数据时 -> 第二条数据
    # 同1秒只有一条数据 
    df['datetime'] = pd.to_datetime(df.Time)
    latter_indices = (df.Time != df.Time.shift(-1)) & df.datetime.map(lambda x: x.microsecond == 0)
    df.loc[latter_indices, 'datetime'] += datetime.timedelta(seconds=0.5)

    t = pd.to_timedelta(get_trade_time())
    ranges = list(zip(t[0::2], t[1::2]))
    def in_trade_time(x):
        x= datetime.timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)

        return any(map(lambda r: r[0] <= x and x <= r[1], ranges))

    df = df[df.datetime.map(in_trade_time)]
    df.index = df.datetime

    return df

def tick2min(df):
    resampler = df.resample('1min', closed='right', label='left')
    df = resampler.LastClose.ohlc()
    return df

def raw2min(df):
    df = raw2tick(df)
    df = tick2min(df)

df = pd.read_csv('./OP10000969.csv', encoding='gb2312')

df = raw2tick(df)
df

# %%
