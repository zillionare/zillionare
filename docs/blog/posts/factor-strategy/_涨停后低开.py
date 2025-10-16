# 克隆自聚宽文章：https://www.joinquant.com/post/44901
# 标题：首板低开策略
# 作者：wywy1995

from jqlib.technical_analysis import *
from jqfactor import *
from jqdata import *
import datetime as dt
import pandas as pd



def initialize(context):
    # 系统设置
    set_option('use_real_price', True)
    set_option('avoid_future_data', True)
    log.set_level('system', 'error')
    # 每日运行
    run_daily(buy, '09:30') #9:25分知道开盘价后可以提前下单
    run_daily(sell, '11:28')
    run_daily(sell, '14:50')



# 选股
def buy(context):
    
    # 基础信息
    date = transform_date(context.previous_date, 'str')
    current_data = get_current_data()
    
    # 昨日涨停列表
    initial_list = prepare_stock_list(date)
    hl_list = get_hl_stock(initial_list, date)
    
    if len(hl_list) != 0:    
        # 获取非连板涨停的股票
        ccd = get_continue_count_df(hl_list, date, 10)
        lb_list = list(ccd.index)
        stock_list = [s for s in hl_list if s not in lb_list]
        
        # 计算相对位置
        rpd = get_relative_position_df(stock_list, date, 60)
        rpd = rpd[rpd['rp'] <= 0.5]
        stock_list = list(rpd.index)
        
        # 低开
        df =  get_price(stock_list, end_date=date, frequency='daily', fields=['close'], count=1, panel=False, fill_paused=False, skip_paused=True).set_index('code') if len(stock_list) != 0 else pd.DataFrame()
        df['open_pct'] = [current_data[s].day_open/df.loc[s, 'close'] for s in stock_list]
        df = df[(0.96 <= df['open_pct']) & (df['open_pct'] <= 0.97)] #低开越多风险越大，选择3个多点即可
        stock_list = list(df.index)
        
        # 买入
        if len(context.portfolio.positions) == 0:
            for s in stock_list:
                order_target_value(s, context.portfolio.total_value/len(stock_list))
                print( '买入', [get_security_info(s, date).display_name, s])
                print('———————————————————————————————————')



def sell(context):
    
    # 基础信息
    date = transform_date(context.previous_date, 'str')
    current_data = get_current_data()
    
    # 根据时间执行不同的卖出策略
    if str(context.current_dt)[-8:] == '11:28:00':
        for s in list(context.portfolio.positions):
            if ((context.portfolio.positions[s].closeable_amount != 0) and (current_data[s].last_price < current_data[s].high_limit) and (current_data[s].last_price > context.portfolio.positions[s].avg_cost)):
                order_target_value(s, 0)
                print( '止盈卖出', [get_security_info(s, date).display_name, s])
                print('———————————————————————————————————')
    
    if str(context.current_dt)[-8:] == '14:50:00':
        for s in list(context.portfolio.positions):
            if ((context.portfolio.positions[s].closeable_amount != 0) and (current_data[s].last_price < current_data[s].high_limit)):
                order_target_value(s, 0)
                print( '止损卖出', [get_security_info(s, date).display_name, s])
                print('———————————————————————————————————')


############################################################################################################################################################################

# 处理日期相关函数
def transform_date(date, date_type):
    if type(date) == str:
        str_date = date
        dt_date = dt.datetime.strptime(date, '%Y-%m-%d')
        d_date = dt_date.date()
    elif type(date) == dt.datetime:
        str_date = date.strftime('%Y-%m-%d')
        dt_date = date
        d_date = dt_date.date()
    elif type(date) == dt.date:
        str_date = date.strftime('%Y-%m-%d')
        dt_date = dt.datetime.strptime(str_date, '%Y-%m-%d')
        d_date = date
    dct = {'str':str_date, 'dt':dt_date, 'd':d_date}
    return dct[date_type]

def get_shifted_date(date, days, days_type='T'):
    #获取上一个自然日
    d_date = transform_date(date, 'd')
    yesterday = d_date + dt.timedelta(-1)
    #移动days个自然日
    if days_type == 'N':
        shifted_date = yesterday + dt.timedelta(days+1)
    #移动days个交易日
    if days_type == 'T':
        all_trade_days = [i.strftime('%Y-%m-%d') for i in list(get_all_trade_days())]
        #如果上一个自然日是交易日，根据其在交易日列表中的index计算平移后的交易日        
        if str(yesterday) in all_trade_days:
            shifted_date = all_trade_days[all_trade_days.index(str(yesterday)) + days + 1]
        #否则，从上一个自然日向前数，先找到最近一个交易日，再开始平移
        else: #否则，从上一个自然日向前数，先找到最近一个交易日，再开始平移
            for i in range(100):
                last_trade_date = yesterday - dt.timedelta(i)
                if str(last_trade_date) in all_trade_days:
                    shifted_date = all_trade_days[all_trade_days.index(str(last_trade_date)) + days + 1]
                    break
    return str(shifted_date)



# 过滤函数
def filter_new_stock(initial_list, date, days=250):
    d_date = transform_date(date, 'd')
    return [stock for stock in initial_list if d_date - get_security_info(stock).start_date > dt.timedelta(days=days)]

def filter_st_stock(initial_list, date):
    str_date = transform_date(date, 'str')
    if get_shifted_date(str_date, 0, 'N') != get_shifted_date(str_date, 0, 'T'):
        str_date = get_shifted_date(str_date, -1, 'T')
    df = get_extras('is_st', initial_list, start_date=str_date, end_date=str_date, df=True)
    df = df.T
    df.columns = ['is_st']
    df = df[df['is_st'] == False]
    filter_list = list(df.index)
    return filter_list

def filter_kcbj_stock(initial_list):
    return [stock for stock in initial_list if stock[0] != '4' and stock[0] != '8' and stock[:2] != '68']

def filter_paused_stock(initial_list, date):
    df = get_price(initial_list, end_date=date, frequency='daily', fields=['paused'], count=1, panel=False, fill_paused=True)
    df = df[df['paused'] == 0]
    paused_list = list(df.code)
    return paused_list



# 每日初始股票池
def prepare_stock_list(date): 
    initial_list = get_all_securities('stock', date).index.tolist()
    initial_list = filter_kcbj_stock(initial_list)
    initial_list = filter_new_stock(initial_list, date)
    initial_list = filter_st_stock(initial_list, date)
    initial_list = filter_paused_stock(initial_list, date)
    return initial_list

# 筛选出某一日涨停的股票
def get_hl_stock(initial_list, date):
    df = get_price(initial_list, end_date=date, frequency='daily', fields=['close','high','high_limit'], count=1, panel=False, fill_paused=False, skip_paused=False)
    df = df.dropna() #去除停牌
    df = df[df['close'] == df['high_limit']]
    hl_list = list(df.code)
    return hl_list

# 计算涨停数
def get_hl_count_df(hl_list, date, watch_days):
    # 获取watch_days的数据
    df = get_price(hl_list, end_date=date, frequency='daily', fields=['low','close','high_limit'], count=watch_days, panel=False, fill_paused=False, skip_paused=False)
    df.index = df.code
    #计算涨停与一字涨停数，一字涨停定义为最低价等于涨停价
    hl_count_list = []
    extreme_hl_count_list = []
    for stock in hl_list:
        df_sub = df.loc[stock]
        hl_days = df_sub[df_sub.close==df_sub.high_limit].high_limit.count()
        extreme_hl_days = df_sub[df_sub.low==df_sub.high_limit].high_limit.count()
        hl_count_list.append(hl_days)
        extreme_hl_count_list.append(extreme_hl_days)
    #创建df记录
    df = pd.DataFrame(index=hl_list, data={'count':hl_count_list, 'extreme_count':extreme_hl_count_list})
    return df

# 计算连板数
def get_continue_count_df(hl_list, date, watch_days):
    df = pd.DataFrame()
    for d in range(2, watch_days+1):
        HLC = get_hl_count_df(hl_list, date, d)
        CHLC = HLC[HLC['count'] == d]
        df = df.append(CHLC)
    stock_list = list(set(df.index))
    ccd = pd.DataFrame()
    for s in stock_list:
        tmp = df.loc[[s]]
        if len(tmp) > 1:
            M = tmp['count'].max()
            tmp = tmp[tmp['count'] == M]
        ccd = ccd.append(tmp)
    if len(ccd) != 0:
        ccd = ccd.sort_values(by='count', ascending=False)    
    return ccd

# 计算股票处于一段时间内相对位置
def get_relative_position_df(stock_list, date, watch_days):
    if len(stock_list) != 0:
        df = get_price(stock_list, end_date=date, fields=['high', 'low', 'close'], count=watch_days, fill_paused=False, skip_paused=False, panel=False).dropna()
        close = df.groupby('code').apply(lambda df: df.iloc[-1,-1])
        high = df.groupby('code').apply(lambda df: df['high'].max())
        low = df.groupby('code').apply(lambda df: df['low'].min())
        result = pd.DataFrame()
        result['rp'] = (close-low) / (high-low)
        return result
    else:
        return pd.DataFrame(columns=['rp'])
