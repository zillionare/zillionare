# 克隆自聚宽文章：https://www.joinquant.com/post/62378
# 标题：年化214%-回撤13% --- 国九条+KDJ+RSRS
# 作者：蛋仔9

# 克隆自聚宽文章：https://www.joinquant.com/post/62222
# 标题：牛市最强策略之一
# 作者：chenjp

# 克隆自聚宽文章：https://www.joinquant.com/post/61675
# 标题：又没积分了，长周期KDJ+国九条优化版
# 作者：M发际线

# 克隆自聚宽文章：https://www.joinquant.com/post/61675
# 标题：又没积分了，长周期KDJ+国九条优化版
# 作者：M发际线

import json
import random
import time
from datetime import date
from datetime import datetime as dt
from datetime import time

import numpy as np
import pandas as pd
from jqdata import *
from jqdata import finance
from jqfactor import *


# ==================== 初始化函数 ====================
def initialize(context):
    pass

def after_code_changed(context):
    # 基础设置
    unschedule_all()  # 清空所有定时任务
    set_option('avoid_future_data', True)  # 开启防未来函数
    set_benchmark('399101.XSHE')  # 设定基准
    set_option('use_real_price', True)  # 用真实价格交易
    # 固定滑点设置ETF 0.001(即交易对手方一档价)
    set_slippage(FixedSlippage(0.002), type="fund")
    # 股票交易总成本0.3%(含固定滑点0.02)
    set_slippage(FixedSlippage(0.02), type="stock")
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            close_today_commission=0,
            min_commission=5,
        ),
        type="stock",
    )
    # 设置货币ETF交易佣金0
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0,
            open_commission=0,
            close_commission=0,
            close_today_commission=0,
            min_commission=0,
        ),
        type="mmf",
    )
    # 日志设置
    log.set_level('order', 'error')
    log.set_level('system', 'error')
    log.set_level('strategy', 'debug')
    
    # 全局变量初始化
    g.ref_stock = '000300.XSHG'  # 择时计算的基础数据
    
    # 布尔类型全局变量
    g.trading_signal = True  # 是否为可交易日
    g.run_stoploss = True  # 是否进行止损
    g.filter_audit = False  # 是否筛选审计意见
    # g.adjust_num = False  # 是否调整持仓数量 (Currently unused)
    
    # 列表类型全局变量
    g.hold_list = []  # 当前持仓的全部股票    
    g.yesterday_HL_list = []  # 记录持仓中昨日涨停的股票
    g.target_list = []
    g.pass_months = [1, 4]  # 空仓的月份
    # g.limitup_stocks = []  # 记录涨停的股票避免再次买入 (Reset in prepare_stock_list but not used for filtering)
    
    # 数值类型全局变量
    g.min_mv = 10  # 股票最小市值要求
    g.max_mv = 500  # 股票最大市值要求
    g.stock_num = 4  # 持股数量 6
    g.etf_num = 1  # ETF数量
    # g.last_trade_date = None  # 记录交易日期 (Currently not updated)
    # g.count_days = 0  # 空仓期计数器 (Set in check_holdings_decline but not read)
    # g.watch_days = 15  # 空仓期阈值 (Currently unused)
    
    # 止损相关设置
    g.stoploss_list = []  # 止损卖出列表 (Appended in stop_loss but not read)
    g.other_sale = []  # 其他卖出列表 (Appended in stop_loss but not read)
    g.stoploss_strategy = 1  # 1为止损线止损，2为市场趋势止损, 3为联合1、2策略
    g.stoploss_limit = 0.09  # 止损线
    g.stoploss_market = 0.05  # 市场趋势止损参数
    g.highest = 100  # 股票单价上限设置
       
    # ETF相关设置
    g.money_etf = '511880.XSHG'  # 空仓月份持有银华日利ETF
    g.stock_pool = [
        #'510050.XSHG', # 上证50ETF
        '159928.XSHE', # 中证消费ETF
        #'510300.XSHG', # 沪深300ETF
        '159949.XSHE', # 创业板50ETF
        #'588080.XSHG', # 科创50ETF
        #'159783.XSHE', # 双创ETF
        '518880.XSHG', # 黄金ETF
        '159561.XSHE', # 德国ETF
        #'510500.XSHG',  # 中证500ETF
        #'159985.XSHE'  # 豆粕etf
    ]
    
    # ETF动量参数设置
    g.momentum_day = 20  # 最新动量参考天数
    # g.score_threshold = 0.5  # 动量因子阈值 - Overwritten by the next line
    g.N = 18  # 计算最新斜率slope，拟合度r2参考天数
    g.M = 600  # 计算最新标准分zscore，rsrs_score参考天数
    g.score_threshold = 0.7  # rsrs标准分指标阈值
    g.mean_day = 30  # 计算结束ma收盘价参考天数
    g.mean_diff_day = 2  # 计算初始ma收盘价参考天数
    g.slope_series = initial_slope_series()[:-1]  # 除去回测第一天的slope
    
    # 其他参数设置
    g.sold_stock_record = {}
    g.max_industry_stocks = 2
    g.record_days = 10

    g.KDJ_signal = 'KEEP'
    g.etf_buy_block_days = 0
    g.trading_signal = True
    g.count_days = 0
    g.sell_signal = 'KEEP'
    g.random_days = 0
    g.run_random_days = False
    
    # 设置定时任务
    run_daily(prepare_stock_list, '9:05')  # 准备股票池
    run_daily(my_trade, '9:30')  # ETF交易逻辑
    run_daily(trade_afternoon, time='14:00', reference_security='399101.XSHE')  # 下午交易检查
    run_daily(stop_loss, time='09:35')  # 止损检查
    run_daily(stop_loss, time='11:25')  # 止损检查
    run_daily(stop_loss, time='14:55')  # 止损检查
    #run_daily(close_account, '10:10')  # 清仓检查
    run_weekly(weekly_adjustment, 1, '09:35')  # 每周调仓
    run_daily(daily_check, '09:35') #随机选择调仓日期，从9:50改到现值
    run_daily(trading_signal, "09:00")  # 交易信号检查
    # run_daily(check_signal_change, "09:35")  # 信号变化检查
    # 尾盘检查是不是应该卖出持有标的
    run_daily(check_and_sell_at_close, "14:55:30")
    run_daily(update_etf_buy_block_days, "09:27")
    
    # 打印初始状态
    print_position_info(context)
    log.info('账户可用资金：', context.portfolio.subportfolios[0].available_cash)
    log.info('今天的交易信号为：', g.trading_signal)

# ==================== 选股逻辑 ====================
def prepare_stock_list(context):
    """准备股票池，获取已持有列表和昨日涨停列表"""
    g.limitup_stocks = []
    g.hold_list = list(context.portfolio.positions)
    
    # 获取昨日涨停列表
    if g.hold_list:
        df = get_price(g.hold_list, end_date=context.previous_date, frequency='daily', 
                      fields=['close','high_limit','low_limit'], count=1, panel=False, fill_paused=False)
        df = df[df['close'] == df['high_limit']]
        g.yesterday_HL_list = df['code'].tolist()
    else:
        g.yesterday_HL_list = []
    
    # 获取目标股票列表
    # g.target_list = get_stock_list(context)[:g.stock_num]
    target_stock_list = get_stock_list(context)
    log.info('target_stock_list: {}'.format(target_stock_list))
    g.target_list = target_stock_list[:g.stock_num]
    
    # 记录交易信号
    #record(signal=g.trading_signal)

def get_stock_list(context):
    """主要选股逻辑"""
    final_list = []
    MKT_index = '399101.XSHE'
    initial_list = filter_stocks(context, get_index_stocks(MKT_index))
    # log.info('get_stock_list, initial_list: {}'.format(initial_list)) 
    
    # 基本面筛选
    q = query(
        valuation.code,
        indicator.eps,
        valuation.market_cap,
        income.np_parent_company_owners,
        income.net_profit,
        income.operating_revenue
    ).filter(
        valuation.code.in_(initial_list),
        indicator.eps > 0,
        valuation.market_cap.between(g.min_mv, g.max_mv),
        income.np_parent_company_owners > 0,
        income.net_profit > 0,
        income.operating_revenue > 1e8
    ).order_by(valuation.market_cap.asc()).limit(g.stock_num*3)
    
    df = get_fundamentals(q)
    
    log.info('final_list 1: {}'.format(df['code'].tolist()))
    
    # 审计意见筛选
    if g.filter_audit:
        before_audit_filter = len(df)
        df['audit'] = df['code'].apply(lambda x: filter_audit(context, x))
        df_audit = df[df['audit'] == True]
        log.info('去除掉了存在审计问题的股票{}只'.format(len(df)-before_audit_filter))
    
    final_list = df['code'].tolist()
    log.info('final_list 1-1: {}'.format(final_list))
    
    # 过滤最近卖出的股票
    recently_sold_stocks = [stock for date in g.sold_stock_record for stock in g.sold_stock_record[date]]
    final_list = [stock for stock in final_list if stock not in recently_sold_stocks]
    log.info('final_list 2: {}'.format(final_list))
    
    # 行业分散
    industry_info = hyxx(final_list)
    final_list = hyxz(final_list, industry_info, g.max_industry_stocks)
    log.info('final_list 3: {}'.format(final_list))
    
    # 价格筛选
    if final_list:
        last_prices = history(1, unit='1d', field='close', security_list=final_list)
        final_list = [stock for stock in final_list if stock in g.hold_list or last_prices[stock][-1] <= g.highest]
        
        log.info('final_list 4: {}'.format(final_list))
        return final_list
    else:
        log.info('无适合股票，买入ETF')
        return []

def filter_stocks(context, stock_list):
    """过滤股票的基本条件"""
    current_data = get_current_data()
    last_prices = history(1, unit='1m', field='close', security_list=stock_list)
    filtered_stocks = []
    
    for stock in stock_list:
        # 基本条件过滤
        if current_data[stock].paused:  # 停牌
            continue
        if current_data[stock].is_st:  # ST
            continue
        if '退' in current_data[stock].name:  # 退市
            continue
        if stock.startswith('30') or stock.startswith('68') or stock.startswith('8') or stock.startswith('4') or stock.startswith('9'):  # 市场类型
            continue
        if not (stock in context.portfolio.positions or last_prices[stock][-1] < current_data[stock].high_limit):  # 涨停
            continue
        if not (stock in context.portfolio.positions or last_prices[stock][-1] > current_data[stock].low_limit):  # 跌停
            continue
            
        # 次新股过滤
        start_date = get_security_info(stock).start_date
        if context.previous_date - start_date < datetime.timedelta(days=375):
            continue
            
        filtered_stocks.append(stock)
    return filtered_stocks

def filter_audit(context, code):
    """筛选审计意见"""
    lstd = context.previous_date
    last_year = lstd.replace(year=lstd.year - 3, month=1, day=1)
    q = query(finance.STK_AUDIT_OPINION.code, finance.STK_AUDIT_OPINION.report_type
          ).filter(finance.STK_AUDIT_OPINION.code==code, finance.STK_AUDIT_OPINION.pub_date>=last_year)
    df = finance.run_query(q)
    df['report_type'] = df['report_type'].astype(str)
    contains_nums = df['report_type'].str.contains(r'2|3|4|5')
    return not contains_nums.any()

# ==================== 交易逻辑 ====================
def my_trade(context):
    """主要交易逻辑 - Handles ETF trading when stock trading signal is off"""
    if g.trading_signal == False:
        hour = context.current_dt.hour
        minute = context.current_dt.minute
        if hour == 9 and minute == 30:
            # Get the target ETF based on rank
            target_etf_rank = get_rank(context, g.stock_pool) # Returns ['ETF_CODE', score]
            target_etf = target_etf_rank[0] # Extract just the ETF code
            g.target_list = [target_etf] # Store the target ETF code in target_list
            
            timing_signal = get_timing_signal(context, g.ref_stock)
            print('今日自选ETF及择时信号:{} {}'.format(target_etf, timing_signal))
            
            current_positions = context.portfolio.positions
            
            if timing_signal == 'SELL':
                # Sell all holdings if timing signal is SELL
                log.info("择时信号为SELL，清仓所有头寸")
                for stock in list(current_positions.keys()):
                    position = current_positions[stock]
                    close_position(context, position)
            elif timing_signal == 'BUY' or timing_signal == 'KEEP':
                # Sell holdings that are not the target ETF
                for stock in list(current_positions.keys()):
                    if stock != target_etf:
                        log.info("[%s]已不在目标ETF列表中，卖出" % (stock))
                        position = current_positions[stock]
                        close_position(context, position)
                    # else: # Optional: Keep the target ETF if already held
                    #     log.info("[%s]已持有目标ETF，无需重复买入" % (stock))

                # Buy the target ETF if not already held sufficiently
                position_count = len(context.portfolio.positions) # Re-check after selling
                cash_available = context.portfolio.available_cash
                target_etf_position = current_positions.get(target_etf)

                # Buy if not holding the target ETF or holding zero amount
                if cash_available > 0 and (target_etf_position is None or target_etf_position.total_amount == 0):
                     # Check if we still need to reach the target ETF number (usually 1)
                     if g.etf_num > position_count:
                         value = cash_available / (g.etf_num - position_count) # Allocate remaining cash
                         log.info("买入目标ETF [%s]（%s元）" % (target_etf, value))
                         order_target_value(target_etf, value)

def weekly_adjustment(context):
    """每周调仓逻辑 - Handles stock trading when trading signal is ON"""
    if g.trading_signal:
        # Ensure g.target_list contains stocks from get_stock_list
        # Note: prepare_stock_list already updates g.target_list daily if g.trading_signal is True
        
        sell_list = [stock for stock in g.hold_list if stock not in g.target_list and stock not in g.yesterday_HL_list]
        hold_list = [stock for stock in g.hold_list if stock in g.target_list or stock in g.yesterday_HL_list]
        log.info("计划卖出(非目标且非昨日涨停):[%s]" % (str(sell_list)))
        log.info("计划保留(目标或昨日涨停):[%s]" % (str(hold_list)))
        
        # 卖出不在目标列表中的股票 (and not yesterday's limit up)
        current_positions = context.portfolio.positions
        for stock in sell_list: # Iterate directly over the calculated sell_list
            if stock in current_positions: # Check if actually holding before selling
                position = current_positions[stock]
                close_position(context, position)
            
        # 买入新的目标股票 (that are not currently held)
        buy_list = [stock for stock in g.target_list if stock not in g.hold_list]
        log.info("计划买入(新目标):[%s]" % (str(buy_list)))
        buy_security(context, buy_list, g.stock_num - len(hold_list)) # Adjust number to buy based on target and current holds

def daily_check(context):
    if g.run_random_days:
        g.random_days -=1
        if g.random_days==0:
            g.random_days = random.randint(1, 6)
            weekly_adjustment(context)
        else:
            pass

def buy_security(context, target_list, num_to_buy):
    """买入证券 (Stocks)"""
    position_count = len(context.portfolio.positions)
    target_buy_count = num_to_buy # Use calculated number to buy
    
    # Calculate value per stock based on available cash and number to buy
    if target_buy_count > 0 and context.portfolio.available_cash > 0:
        value_per_stock = context.portfolio.available_cash / target_buy_count
        
        bought_count = 0
        for stock in target_list:
            if bought_count >= target_buy_count: # Stop if we've bought enough
                 break
            # Check if we have enough cash for minimum order (simple check)
            if context.portfolio.available_cash < 1000: # Assuming a minimum value needed
                 log.warning("现金不足，无法继续买入 %s" % stock)
                 break
            
            # Place order
            order = order_target_value(stock, value_per_stock)
            if order is not None and order.filled > 0:
                log.info("买入[%s]（目标价值 %.2f元）" % (stock, value_per_stock))
                bought_count += 1
                # Optional: recalculate value_per_stock if needed after cash is used
            elif order is None:
                 log.error("尝试买入 [%s] 时下单失败" % stock)
            
            # Check if reached max stock number (redundant if target_buy_count is correct, but safe)
            if len(context.portfolio.positions) >= g.stock_num:
                break
    elif target_buy_count <= 0:
        log.info("无需买入新的股票。")

def close_position(context, position):
    """平仓操作"""
    security = position.security
    amount = position.total_amount   
    order = order_target_value(security, 0)
    if order is not None:
        if order.status == OrderStatus.held and order.filled == order.amount:
            record_recently_sold_stocks(context, security)
            return True
    return False

def close_account(context):
    """
    清仓函数，在交易信号为False时执行
    """
    if not g.trading_signal:
        curr_data = get_current_data()
        current_positions = context.portfolio.positions
        
        # 遍历所有持仓
        if len(g.hold_list) > 0 and g.hold_list != [g.money_etf]:
            # Iterate over a copy of keys to avoid modification issues
            for stock in list(current_positions.keys()): 
                # Ensure we have position data (should always be true if iterating keys)
                if stock not in current_positions: 
                    continue 
                    
                position = current_positions[stock]
                amount = position.total_amount 
                
                # 跳过特殊情况
                if stock == g.money_etf:  # 跳过货币ETF
                    continue
                # When trading_signal is False, g.target_list should contain the target ETF from my_trade
                if stock in g.target_list:  # 跳过目标列表中的ETF (allow holding the target ETF)
                    continue
                # Check for hardcoded index - review if this is still needed
                # if stock in get_index_stocks('399411.XSHE'):  
                #     continue
                if stock not in curr_data: # Handle case where stock data might be missing
                    log.warning(f"无法获取 {stock} 的当前数据，跳过清仓检查")
                    continue
                if curr_data[stock].last_price <= curr_data[stock].low_limit or curr_data[stock].paused:  # 跳过跌停或停牌股票
                    continue
                
                # 执行清仓
                log.info("交易信号为False，清仓非目标ETF [%s]" % (stock))
                close_position(context, position) # Use close_position for consistency

# ==================== 风控逻辑 ====================
def stop_loss(context):
    """止损逻辑"""
    if g.run_stoploss:
        current_positions = context.portfolio.positions
        
        # 个股止损策略
        if g.stoploss_strategy == 1 or g.stoploss_strategy == 3:
            for stock in current_positions.keys():
                price = current_positions[stock].price
                avg_cost = current_positions[stock].avg_cost
                amount = current_positions[stock].total_amount
                
                # 个股盈利止盈
                if price >= avg_cost * 2:
                    close_position(context, current_positions[stock])
                    g.other_sale.append(stock)
                # 个股止损
                elif price < avg_cost * (1 - g.stoploss_limit):
                    close_position(context, current_positions[stock])
                    g.other_sale.append(stock)
                    log.debug("收益止损,卖出{}".format(stock))
                    g.stoploss_list.append(stock)
        
        # 市场趋势止损策略
        if g.stoploss_strategy == 2 or g.stoploss_strategy == 3:
            stock_df = get_price(security=get_index_stocks('399101.XSHE'),
                               end_date=context.previous_date, frequency='daily',
                               fields=['close', 'open'], count=1, panel=False)
            down_ratio = (1 - stock_df['close'] / stock_df['open']).mean()
            
            if down_ratio >= g.stoploss_market:
                for stock in current_positions.keys():
                    amount = current_positions[stock].total_amount
                    g.stoploss_list.append(stock)
                    log.debug("大盘惨跌,平均降幅{:.2%}".format(down_ratio))
                    close_position(context, current_positions[stock])
                    g.other_sale.append(stock)

def check_holdings_decline(context):
    """检查持仓标的的价格变化情况"""
    positions = context.portfolio.positions
    
    if not positions:
        return False
    
    stocks = list(positions.keys())
    price_data = history(2, unit='1d', field='close', security_list=stocks)
    
    decline_count = 0
    for stock in stocks:
        yesterday_price = price_data[stock][0]
        today_price = price_data[stock][1]
        if (today_price - yesterday_price) / yesterday_price < -0.01:
            decline_count += 1
    
    decline_ratio = decline_count / len(stocks)
    
    if decline_ratio >= 0.9:
        g.trading_signal = False
        g.count_days = 1
        log.info(f"触发清仓信号：{decline_ratio:.2%}的持仓股票下跌超过1%")
        return True
    
    return False

# ==================== 辅助函数 ====================
def record_recently_sold_stocks(context, stock):
    """记录最近卖出的股票"""
    # Only record sold stocks, not ETFs from g.stock_pool
    if stock not in g.stock_pool: 
        current_date = context.current_dt.date()
        
        if current_date not in g.sold_stock_record:
            g.sold_stock_record[current_date] = []
        g.sold_stock_record[current_date].append(stock)
    
        trade_days = get_trade_days(start_date=current_date - datetime.timedelta(days=g.record_days), end_date=current_date)
        for date in list(g.sold_stock_record.keys()):
            if date not in trade_days:
                del g.sold_stock_record[date]

def hyxx(stocks):
    """获取行业信息"""
    industry_data = get_industry(stocks, date=None)  
    return pd.Series({stock: industry_data[stock]['sw_l1']['industry_name'] if 'sw_l1' in industry_data[stock] else None for stock in stocks})

def hyxz(stocks, industry_info, max_industry_stocks):
    """行业分散"""
    if industry_info is None:
        return stocks
    counts = {}
    result = []
    for stock in stocks:
        industry = industry_info[stock]
        if counts.get(industry, 0) < max_industry_stocks:
            result.append(stock)
            counts[industry] = counts.get(industry, 0) + 1
    return result

def print_position_info(context):
    """打印持仓信息"""
    for position in list(context.portfolio.positions.values()):
        securities = position.security
        cost = position.avg_cost
        price = position.price
        ret = 100*(price/cost-1)
        value = position.value
        amount = position.total_amount    
        print('代码:{}'.format(securities))
        print('成本价:{}'.format(format(cost,'.2f')))
        print('现价:{}'.format(price))
        print('收益率:{}%'.format(format(ret,'.2f')))
        print('持仓(股):{}'.format(amount))
        print('市值:{}'.format(format(value,'.2f')))
    print('———————————————————————————————————————分割线————————————————————————————————————————')

# ==================== ETF动量策略相关函数 ====================
def get_rank(context, stock_pool):
    """计算ETF动量排名, 返回最佳ETF代码和分数: ['CODE', score]"""
    rank = []
    if not g.stock_pool:  # Handle empty pool
        log.error("ETF stock pool (g.stock_pool) is empty.")
        return [None, -np.inf]  # Return placeholder indicating error or no result

    etf_data_log = {}  # To store data for logging
    for etf_code in g.stock_pool:
        # Fetch history safely
        try:
            data = attribute_history(etf_code, g.momentum_day, '1d', ['close'], df=True, skip_paused=True)
            if data is None or data.empty or len(data) < 2:  # Need at least 2 points for polyfit
                log.warning(f"无法获取足够的价格数据用于动量计算: {etf_code}, 跳过。")
                continue
            
            # Ensure close prices are valid
            if data.close.isnull().any() or not np.all(np.isfinite(data.close)):
                log.warning(f"价格数据包含无效值: {etf_code}, 跳过。")
                continue
            
            # Normalize prices relative to the start; handle potential zero division
            start_price = data.close.iloc[0]
            if start_price == 0:
                log.warning(f"起始价格为零: {etf_code}, 跳过。")
                continue
            normalized_prices = data.close / start_price
            
            # Calculate momentum score (slope)
            score = np.polyfit(np.arange(len(normalized_prices)), normalized_prices, 1)[0]
            rank.append([etf_code, score])
            etf_data_log[etf_code] = data  # Store data for logging
            
        except Exception as e:
            log.error(f"计算ETF动量时出错 {etf_code}: {e}")
            continue  # Skip this ETF on error

    if not rank:  # Handle case where no ETF could be ranked
        log.error("无法为任何ETF计算动量排名。")
        return [None, -np.inf]
    
    rank.sort(key=lambda x: x[1], reverse=True)  # Sort by score descending
    
    # Log info for the top ranked ETF
    top_etf_code = rank[0][0]
    if top_etf_code in etf_data_log:
        log.info(f"最佳动量 ETF: {top_etf_code} (Score: {rank[0][1]:.4f})")
        log.info(f"其最近 {g.momentum_day} 天收盘价数据:\n{etf_data_log[top_etf_code].tail(3)}")
    else:
        log.info(f"最佳动量 ETF: {top_etf_code} (Score: {rank[0][1]:.4f}) (无详细数据记录)")

    return rank[0]  # Return the top [CODE, score]

def get_ols(x, y):
    """计算OLS回归"""
    slope, intercept = np.polyfit(x, y, 1)
    r2 = 1 - (sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
    return (intercept, slope, r2)

def initial_slope_series():
    """初始化斜率序列"""
    data = attribute_history(g.ref_stock, g.N + g.M, '1d', ['high', 'low'])
    return [get_ols(data.low[i:i+g.N], data.high[i:i+g.N])[1] for i in range(g.M)]

def get_zscore(slope_series):
    """计算Z分数"""
    mean = np.mean(slope_series)
    std = np.std(slope_series)
    return (slope_series[-1] - mean) / std

def get_timing_signal(context, stock):
    """获取择时信号"""
    g.mean_diff_day = 5
    close_data = attribute_history(g.ref_stock, g.mean_day + g.mean_diff_day, '1d', ['close'])
    high_low_data = attribute_history(g.ref_stock, g.N, '1d', ['high', 'low'])

    intercept, slope, r2 = get_ols(high_low_data.low, high_low_data.high)
    g.slope_series.append(slope)
    rsrs_score = get_zscore(g.slope_series[-g.M:]) * r2
    
    if rsrs_score > g.score_threshold: 
        return "BUY"
    elif rsrs_score < -g.score_threshold: 
        return "SELL"
    else: 
        return "KEEP"

def get_timing_signal_with_now_price(context, stock, current_price=None):
    """
    基于原始get_timing_signal的实现，增加当前价格参数的择时信号函数
    参数:
        context: 上下文
        stock: 股票代码
        current_price: 当前价格（可选，如果不提供则使用历史数据）
    返回:
        "BUY", "SELL", 或 "KEEP"
    """
    try:
        g.mean_diff_day = 5
        
        # 获取历史收盘价数据
        close_data = attribute_history(g.ref_stock, g.mean_day + g.mean_diff_day, '1d', ['close'])
        
        # 获取高低价数据用于计算RSRS
        high_low_data = attribute_history(g.ref_stock, g.N, '1d', ['high', 'low'])
        
        # 如果提供了当前价格，可以将其作为最新的收盘价考虑
        # 但RSRS主要基于高低价，所以这里保持原逻辑
        
        # 计算RSRS指标
        intercept, slope, r2 = get_ols(high_low_data.low, high_low_data.high)
        
        # 创建临时slope_series副本，避免修改全局变量
        temp_slope_series = list(g.slope_series)
        temp_slope_series.append(slope)
        
        # 计算RSRS分数
        rsrs_score = get_zscore(temp_slope_series[-g.M:]) * r2
        
        # 如果提供了当前价格，可以在这里加入额外的价格判断逻辑
        if current_price is not None:
            # 获取最近的收盘价进行比较
            recent_close = close_data['close'].iloc[-1]
            price_change_ratio = (current_price - recent_close) / recent_close
            
            # 可以根据价格变化调整信号强度
            # 这里是一个简单的示例，您可以根据需要调整
            if price_change_ratio > 0.02:  # 当前价格比最近收盘价高2%以上
                rsrs_score *= 0.9  # 略微降低买入信号强度
            elif price_change_ratio < -0.02:  # 当前价格比最近收盘价低2%以上
                rsrs_score *= 1.1  # 略微增强信号强度
        
        # 返回信号
        if rsrs_score > g.score_threshold: 
            return "BUY"
        elif rsrs_score < -g.score_threshold: 
            return "SELL"
        else: 
            return "KEEP"
            
    except Exception as e:
        print(f"计算择时信号时出错: {e}")
        return "KEEP"  # 出错时返回保持信号


def trading_signal(context):
    """更新交易信号"""
    # Store previous signal before updating
    if hasattr(g, 'trading_signal'): # Check if it exists first time
         g.previous_trading_signal = g.trading_signal
    else:
         g.previous_trading_signal = True # Assume True initially if not set
    g.sell_signal = get_timing_signal(context, g.ref_stock)
    g.trading_signal = market_condition(context)
    # 记录g.sell_signal为False的状态
    if g.sell_signal == 'SELL':
        record(sell_signal=100)
    else:
        record(sell_signal=0)
    # 记录g.trading_signal的True和False状态
    if g.trading_signal == True:
        record(trading_signal=100)
    else:
        record(trading_signal=0)
    
    # Log the signal
    if g.trading_signal:
        log.info("择时信号: True (继续交易)")
    else:
        log.info("择时信号: False (清仓或转ETF)")
        
    #record(signal=int(g.trading_signal)) # Record 1 for True, 0 for False

def check_signal_change(context):
    """检查信号变化, 若从False变为True, 执行周调仓"""
    # Ensure previous_trading_signal exists
    if not hasattr(g, 'previous_trading_signal'):
        g.previous_trading_signal = g.trading_signal # Initialize if first run

    if g.previous_trading_signal == False and g.trading_signal == True:
        log.info("交易信号从 False 变为 True，执行周调仓逻辑...")
        weekly_adjustment(context)

# ==================== 新增函数 ====================
def trade_afternoon(context):
    check_limit_up(context)
    check_remain_amount(context)


# 调整昨日涨停股票
def check_limit_up(context):
    now_time = context.current_dt
    if g.yesterday_HL_list != []:
        for stock in g.yesterday_HL_list:
            # 对昨日涨停股票观察到尾盘如不涨停则提前卖出，如果涨停即使不在应买入列表仍暂时持有
            current_data = get_price(stock, end_date=now_time, frequency='1m', fields=['close', 'high_limit'], skip_paused=False, fq='pre', count=1, panel=False, fill_paused=True)
            if current_data.iloc[0, 0] < current_data.iloc[0, 1]:
                log.info("[%s]涨停打开，卖出" % (stock))
                position = context.portfolio.positions[stock]
                close_position(context, position)  # Pass context and position
                g.other_sale.append(stock)
                g.limitup_stocks.append(stock)
            else:
                log.info("[%s]涨停，继续持有" % (stock))

# 如果昨天有股票卖出或者买入失败造成空仓，剩余的金额当日买入
def check_remain_amount(context):
    if g.trading_signal:
        addstock_num = len(g.other_sale)
        loss_num = len(g.stoploss_list)
        empty_num = addstock_num + loss_num
        
        g.hold_list = context.portfolio.positions
        if len(g.hold_list) < g.stock_num:   
            # 计算需要买入的股票数量，止损仓位补足货币etf
            # 可替换下一行代码以更换逻辑：改为将清空仓位全部补足股票，而非原作中止损仓位补充货币etf
            # num_stocks_to_buy = min(empty_num,g.stock_num-len(g.hold_list))
            num_stocks_to_buy = min(addstock_num,g.stock_num-len(g.hold_list))
            target_list = [stock for stock in g.target_list if stock not in g.limitup_stocks][:num_stocks_to_buy]
            log.info('有余额可用'+str(round((context.portfolio.cash),2))+'元。买入'+ str(target_list))
            buy_security(context,target_list,len(target_list))
            if loss_num !=0:
                log.info('有余额可用'+str(round((context.portfolio.cash),2))+'元。买入货币基金'+ str(g.money_etf))
                #buy_security(context,[g.money_etf],loss_num)
        
        g.stoploss_list = []
        g.other_sale    = []

# 根据长周期KDJ判断市场情况   
def market_condition(context):
    """
    早上9:00-9:15执行的市场判断
    使用上一交易日的数据计算g.previous_market_breadth
    注意：市场宽度值现在以百分比形式表示，基于申万一级行业总数计算
    """
    try:
        KDJ_signal = calculate_angle_signal(context)
        
        # 处理KDJ信号为None的情况
        if KDJ_signal is None:
            log.warning("KDJ信号计算失败，保持当前交易信号状态")
            # 如果KDJ信号失败，保持当前状态，但确保有值
            if g.trading_signal is None:
                g.trading_signal = True
                g.count_days = 0
                log.info("KDJ信号失败，设置默认交易信号为True")
        else:
            # 根据KDJ信号和市场宽度进行判断
            if KDJ_signal == 'BUY' or KDJ_signal == 'KEEP':
                g.trading_signal = True
                g.count_days = 0
                    
            elif KDJ_signal == 'SELL':
                g.trading_signal = False
                g.count_days = 1
        
        # 确保g.trading_signal有值
        if g.trading_signal is None:
            g.trading_signal = True
            g.count_days = 0
            log.warning("g.trading_signal为None，设置默认值为True")
        
        # 如果交易信号为False，增加计数天数
        if g.trading_signal == False:
            g.count_days += 1
            log.info(f"保持清仓信号，计数天数: {g.count_days}")
            
            # 如果计数超过15天，强制转为交易信号
            if g.count_days > 15:
                g.trading_signal = True
                g.count_days = 0
                log.info(f"计数超过15天，强制触发交易信号")
                weekly_adjustment(context)
        
        # 最终确保返回值
        return g.trading_signal
        
    except Exception as e:
        log.error(f"早上市场判断出错: {e}")
        # 异常情况下设置默认值
        if not hasattr(g, 'trading_signal') or g.trading_signal is None:
            g.trading_signal = True
            g.count_days = 0
            log.info("异常情况下设置默认交易信号为True")
        return g.trading_signal

def calculate_angle_signal(context, stock_code='399101.XSHE'):
    """
    计算KDJ择时信号
    参数：N=27, M1=9, M2=9 (对应传统KDJ的9,9,9)
    返回：'BUY', 'SELL', 'KEEP' 或 None
    """
    N = 27
    M1 = 9
    M2 = 9
    
    try:
        # 获取足够的历史数据来计算KDJ
        df = get_price(stock_code, 
                      end_date=context.previous_date,
                      count=N+20, # 确保有足够数据计算KDJ
                      frequency='daily', 
                      fields=['close', 'high', 'low'], 
                      skip_paused=True)
    except Exception as e:
        log.error(f"获取数据时出错：{str(e)}")
        return None
    
    if len(df) < N + 3:
        log.error(f"数据不足，需要至少{N+3}天数据，当前只有{len(df)}天")
        return None
    
    # 计算RSV
    low_n = df['low'].rolling(window=N).min()
    high_n = df['high'].rolling(window=N).max()
    rsv = (df['close'] - low_n) / (high_n - low_n) * 100
    
    # 计算K值 (对应M1=9)
    k_values = pd.Series(index=rsv.index, dtype=float)
    k_values.iloc[N-1] = rsv.iloc[N-1]  # 初始值
    
    for i in range(N, len(rsv)):
        if pd.notna(rsv.iloc[i]):
            k_values.iloc[i] = (k_values.iloc[i-1] * (M1-1) + rsv.iloc[i]) / M1
        else:
            k_values.iloc[i] = k_values.iloc[i-1]
    
    # 计算D值 (对应M2=9)
    d_values = pd.Series(index=k_values.index, dtype=float)
    d_values.iloc[N-1] = k_values.iloc[N-1]  # 初始值
    
    for i in range(N, len(k_values)):
        if pd.notna(k_values.iloc[i]):
            d_values.iloc[i] = (d_values.iloc[i-1] * (M2-1) + k_values.iloc[i]) / M2
        else:
            d_values.iloc[i] = d_values.iloc[i-1]
    
    # 计算J值 (J = 3*K - 2*D)
    j_values = 3 * k_values - 2 * d_values
    
    # 获取最后两个时间点的KDJ值
    if len(j_values) < 2:
        log.error("KDJ计算后数据不足")
        return None
    
    # 最后一个J值 (当前)
    last_j = j_values.iloc[-1]
    last_k = k_values.iloc[-1]
    last_d = d_values.iloc[-1]
    record(last_k=last_k, last_j=last_j)
    # 倒数第二个J值 (前一个)
    prev_j = j_values.iloc[-2]
    prev_k = k_values.iloc[-2]
    prev_d = d_values.iloc[-2]
    
    # 检查是否有有效值
    if (pd.isna(last_j) or pd.isna(last_k) or pd.isna(last_d) or 
        pd.isna(prev_j) or pd.isna(prev_k) or pd.isna(prev_d)):
        log.error("KDJ值包含NaN，无法判断信号")
        return None
    
    # 使用全局变量记录上一次的信号状态
    if not hasattr(g, 'last_kdj_signal'):
        g.last_kdj_signal = 'KEEP'  # 初始状态
    
    # 判断逻辑
    # 1. SELL条件：倒数第二个J>70 且 倒数第二个J>倒数第二个K 且 倒数第二个J>倒数第二个D
    #    且 最后一个J<倒数第二个J 且 最后一个J<=最后一个K 且 最后一个J<=最后一个D
    if (prev_j > 70 and 
        prev_j > prev_k and 
        prev_j > prev_d and
        last_j < prev_j and 
        last_j <= last_k and 
        last_j <= last_d):
        g.last_kdj_signal = 'SELL'
        log.info(f"KDJ触发SELL信号 - 前J:{prev_j:.2f}, 前K:{prev_k:.2f}, 前D:{prev_d:.2f}, 当前J:{last_j:.2f}, 当前K:{last_k:.2f}, 当前D:{last_d:.2f}")
        return 'SELL'
    
    # 新增SELL条件：prev_j小于prev_k和prev_d，且last_j<last_k和last_d，且last_j<prev_j且last_j>5
    elif (prev_j < prev_k and 
          prev_j < prev_d and
          last_j < last_k and 
          last_j < last_d and
          last_j < prev_j and 
          last_j > 10):
        g.last_kdj_signal = 'SELL'
        log.info(f"KDJ触发新增SELL信号 - 前J:{prev_j:.2f}, 前K:{prev_k:.2f}, 前D:{prev_d:.2f}, 当前J:{last_j:.2f}, 当前K:{last_k:.2f}, 当前D:{last_d:.2f}")
        return 'SELL'
    # 2. BUY条件：当前J < 0
    elif last_j < 0 or (last_k < 20 and last_k > prev_k):
        g.last_kdj_signal = 'BUY'
        log.info(f"KDJ触发BUY信号 - 当前J:{last_j:.2f}, 当前K:{last_k:.2f}, 当前D:{last_d:.2f}")
        return 'BUY'
    
    # 3. 状态保持逻辑
    else:
        # 如果上一次是BUY且还没触发SELL，保持KEEP
        if g.last_kdj_signal == 'BUY':
            return 'KEEP'
        # 如果上一次是SELL且还没触发BUY，保持SELL
        elif g.last_kdj_signal == 'SELL':
            return 'SELL'
        # 其他情况保持KEEP
        else:
            return 'KEEP'

# 尾盘卖出判断逻辑
def check_and_sell_at_close(context):
    # 检查是否需要卖出
    if hasattr(g, 'trading_signal') and g.trading_signal == False:
        # 获取持仓股票
        positions = list(context.portfolio.positions.keys())
        # 只处理属于g.stock_pool的标的
        for stock in positions:
            if stock in getattr(g, 'stock_pool', [])  or stock in g.target_list:
                # 使用健壮的价格获取函数
                current_price = get_current_price_robust(stock, context)
                
                # 如果无法获取价格，跳过该股票
                if current_price is None:
                    log.warning(f"无法获取{stock}当前价格，跳过尾盘信号判断")
                    continue
                
                # 使用新的get_timing_signal_with_now_price函数
                timing_signal = get_timing_signal_with_now_price(context, stock, current_price=current_price)
                
                if timing_signal not in ['KEEP', 'BUY']:
                    # 清仓该ETF
                    order_target(stock, 0)
                    print(f"尾盘卖出信号：{stock} timing_signal={timing_signal}，执行清仓")
                    # 设置全局参数，停止买入etf两个交易日
                    g.etf_buy_block_days = 3
                else:
                    print(f"尾盘信号检查：{stock} timing_signal={timing_signal}，不清仓")

# 在每日收盘前调用该函数，例如在handle_data或自定义的尾盘调度函数中
# check_and_sell_at_close(context)

# 在my_trade买入etf前增加判断
def can_buy_etf():
    # 如果未设置该参数，允许买入
    if not hasattr(g, 'etf_buy_block_days'):
        return True
    # 如果阻断天数为0，允许买入
    if g.etf_buy_block_days <= 0:
        return True
    # 否则不允许买入
    return False

# 在my_trade函数中买入etf前加如下判断
# if can_buy_etf():
#     # 执行买入etf操作
#     ...
# else:
#     print("因尾盘卖出信号，暂停买入ETF")

# 在每日开盘时减少阻断天数
def update_etf_buy_block_days(context):
    if hasattr(g, 'etf_buy_block_days') and g.etf_buy_block_days > 0:
        g.etf_buy_block_days -= 1

# 获取股票当前价格的健壮函数
def get_current_price_robust(stock, context):
    """
    使用多种方法获取股票当前价格
    参数:
        stock: 股票代码
        context: 上下文
    返回:
        current_price: 当前价格，如果获取失败返回None
    """
    current_price = None
    
    # 方法1：使用get_current_data获取实时价格
    try:
        current_data = get_current_data()
        if stock in current_data and hasattr(current_data[stock], 'last_price') and current_data[stock].last_price > 0:
            current_price = current_data[stock].last_price
            log.info(f"方法1成功获取{stock}当前价格: {current_price}")
            return current_price
    except Exception as e:
        log.warning(f"方法1获取{stock}价格失败: {e}")
    
    # 方法2：使用history获取最新分钟数据
    try:
        recent_prices = history(1, unit='1m', field='close', security_list=[stock])
        if not recent_prices.empty and stock in recent_prices.columns and len(recent_prices[stock]) > 0:
            current_price = recent_prices[stock].iloc[-1]
            log.info(f"方法2成功获取{stock}当前价格: {current_price}")
            return current_price
    except Exception as e:
        log.warning(f"方法2获取{stock}价格失败: {e}")
    
    # 方法3：使用get_price获取最新价格
    try:
        price_data = get_price(stock, count=1, end_date=context.current_dt, frequency='1m', fields=['close'])
        if not price_data.empty and 'close' in price_data.columns:
            current_price = price_data['close'].iloc[-1]
            log.info(f"方法3成功获取{stock}当前价格: {current_price}")
            return current_price
    except Exception as e:
        log.warning(f"方法3获取{stock}价格失败: {e}")
    
    # 方法4：使用日线数据作为备用
    try:
        daily_prices = history(1, unit='1d', field='close', security_list=[stock])
        if not daily_prices.empty and stock in daily_prices.columns and len(daily_prices[stock]) > 0:
            current_price = daily_prices[stock].iloc[-1]
            log.info(f"方法4使用日线数据获取{stock}价格: {current_price}")
            return current_price
    except Exception as e:
        log.warning(f"方法4获取{stock}价格失败: {e}")
    
    # 方法5：从持仓中获取当前价格
    try:
        if stock in context.portfolio.positions:
            position = context.portfolio.positions[stock]
            if hasattr(position, 'price') and position.price > 0:
                current_price = position.price
                log.info(f"方法5从持仓获取{stock}当前价格: {current_price}")
                return current_price
    except Exception as e:
        log.warning(f"方法5获取{stock}价格失败: {e}")
    
    log.error(f"所有方法都无法获取{stock}当前价格")
    return None

# 在每日开盘时调用 update_etf_buy_block_days()    return None

# 在每日开盘时调用 update_etf_buy_block_days()
