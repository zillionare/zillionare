"""博文『打新不中，买新当如何』配套代码
"""
import json
import os
import random
import time
from datetime import datetime, timedelta

import httpx
import pandas as pd
import tushare as ts


def get_tushare_api():
    try:
        # User specified that set_token is not needed in this environment
        return ts.pro_api()
    except Exception as e:
        print(f"Error initializing Tushare API: {e}")
        return None

def to_ts_code(stock_code):
    """
    Convert stock code to Tushare format (e.g., 600000 -> 600000.SH)
    """
    if not stock_code:
        return None
    
    stock_code = str(stock_code)
    if stock_code.startswith('6'):
        return f"{stock_code}.SH"
    elif stock_code.startswith('0') or stock_code.startswith('3'):
        return f"{stock_code}.SZ"
    elif stock_code.startswith('8') or stock_code.startswith('4') or stock_code.startswith('9'):
        return f"{stock_code}.BJ"
    else:
        return stock_code

def get_ipo_data(max_pages=None):
    """
    Fetch IPO data from Eastmoney with pagination.
    Args:
        max_pages (int, optional): Maximum number of pages to fetch. If None, fetch all.
    Returns:
        pandas.DataFrame: Combined data from all fetched pages.
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    
    # Base params
    params = {
        "reportName": "RPTA_APP_IPOAPPLY",
        "columns": "ALL",
        "sortColumns": "APPLY_DATE",
        "sortTypes": "-1",
        "pageSize": "50",
        "filter": "",
        "source": "WEB",
        "client": "WEB"
    }
    
    all_data = []
    page_num = 1
    
    while True:
        print(f"Fetching page {page_num}...")
        params["pageNumber"] = str(page_num)
        
        try:
            response = httpx.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("result"):
                items = data["result"]["data"]
                if not items:
                    print("No more data found.")
                    break
                    
                all_data.extend(items)
                
                total_pages = data["result"]["pages"]
                print(f"Page {page_num} fetched. Total pages: {total_pages}")
                
                # Check exit conditions
                if page_num >= total_pages:
                    break
                    
                if max_pages and page_num >= max_pages:
                    print(f"Reached max pages limit ({max_pages}). Stopping.")
                    break
                
                # Prepare for next page
                page_num += 1
                
                # Random delay between 5 to 10 seconds
                delay = random.uniform(5, 10)
                print(f"Waiting for {delay:.2f} seconds...")
                time.sleep(delay)
                
            else:
                print(f"Error or no result on page {page_num}: {data.get('message')}")
                break
                
        except Exception as e:
            print(f"An error occurred on page {page_num}: {e}")
            break
            
    if not all_data:
        return None
        
    df = pd.DataFrame(all_data)
    
    # Select and rename important columns
    columns_map = {
        "SECURITY_CODE": "股票代码",
        "SECURITY_NAME": "股票简称",
        "TOTAL_ISSUE_NUM": "发行总数",
        "ONLINE_ISSUE_NUM": "网上发行股数",
        "TOP_APPLY_MARKETCAP": "顶格申购需配市值",
        "ONLINE_APPLY_UPPER": "申购上限",
        "ISSUE_PRICE": "发行价格",
        "DILUTED_PE_RATIO": "发行市盈率",
        "INDUSTRY_PE_NEW": "行业市盈率",
        "OFFFLINE_INITIAL_MULTIPLE": "询价累计报价倍数",
        "OFFLINE_EP_OBJECT": "配售对象报价家数",
        "LISTING_DATE": "上市日期",
        "MARKET": "上市板块",
        "ONLINE_ES_MULTIPLE": "网上有效申购倍数",
        "INDUSTRY_NAME": "所属行业",
        "UNDERWRITER_ORG": "保荐机构",
        "TOTAL_SHARES": "总股本",
        "PROFIT": "净利润",
        "NETSUMFINA": "净资产"
    }
    
    # Rename columns that exist
    df = df.rename(columns=columns_map)
    
    # Calculate Valuation Difference (PE Diff)
    # Ensure numeric types
    if "发行市盈率" in df.columns and "行业市盈率" in df.columns:
        df['发行市盈率'] = pd.to_numeric(df['发行市盈率'], errors='coerce')
        df['行业市盈率'] = pd.to_numeric(df['行业市盈率'], errors='coerce')
        df['估值差'] = df['行业市盈率'] - df['发行市盈率']
    
    return df

def analyze_ipo_performance(df):
    """
    Calculate max price increase within 10 days of listing using Tushare.
    """
    pro = get_tushare_api()
    if not pro:
        print("Skipping Tushare analysis due to missing token.")
        return df

    print("Starting Tushare analysis...")
    
    # Add new column
    df['上市10日后最高涨幅'] = None
    
    # Filter for listed stocks
    # Ensure Listing Date is datetime
    # Note: Eastmoney might return dates as strings "YYYY-MM-DD HH:MM:SS" or similar
    
    for index, row in df.iterrows():
        listing_date_str = row.get('上市日期')
        stock_code = row.get('股票代码')
        issue_price = row.get('发行价格')
        
        if not listing_date_str or not stock_code or pd.isna(issue_price):
            continue
            
        try:
            # Parse listing date (assuming format "YYYY-MM-DD ...")
            if isinstance(listing_date_str, str):
                listing_date = datetime.strptime(listing_date_str.split(' ')[0], "%Y-%m-%d")
            else:
                continue
                
            # Skip if listing date is in future
            if listing_date > datetime.now():
                continue
            
            # Check if listing date is less than 14 days from now (10 trading days approx)
            # If so, the observation window is incomplete, so we skip calculation.
            days_since_listing = (datetime.now() - listing_date).days
            if days_since_listing < 14:
                print(f"Skipping {stock_code}: Listed less than 14 days ago ({days_since_listing} days).")
                continue

            # Calculate end date (Listing Date + 14 days to cover 10 trading days)
            end_date = listing_date + timedelta(days=14)
            
            start_date_str = listing_date.strftime("%Y%m%d")
            end_date_str = end_date.strftime("%Y%m%d")
            ts_code = to_ts_code(stock_code)
            
            # Fetch daily data
            # We need to respect Tushare rate limits (usually 200 calls/min for free users?)
            # Let's add a small delay
            # time.sleep(0.3) 
            
            daily_df = pro.daily(ts_code=ts_code, start_date=start_date_str, end_date=end_date_str)
            
            if daily_df is not None and not daily_df.empty:
                max_high = daily_df['high'].max()
                if max_high and issue_price > 0:
                    max_increase = (max_high - issue_price) / issue_price
                    df.at[index, '上市10日后最高涨幅'] = max_increase
                    print(f"Processed {ts_code}: Max High {max_high}, Issue {issue_price}, Increase {max_increase:.2%}")
            else:
                print(f"No daily data for {ts_code}")
                
        except Exception as e:
            print(f"Error processing {stock_code}: {e}")
            
    return df

if __name__ == "__main__":
    print("Starting IPO data fetch ...")
    # 正式获取数据时，请移除 max_pages 参数
    df = get_ipo_data(max_pages=3)
    
    if df is not None:
        print(f"Successfully fetched {len(df)} records.")
        
        # Analyze performance
        df = analyze_ipo_performance(df)
        
        # Save to CSV
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ipo_data.csv")
        # Save only the columns requested by user + performance
        desired_cols = [
            "股票代码", "股票简称", "上市板块", "所属行业", "保荐机构",
            "发行总数", "网上发行股数", "总股本", 
            "顶格申购需配市值", "申购上限", 
            "发行价格", "发行市盈率", "行业市盈率", "估值差",
            "净利润", "净资产",
            "网上有效申购倍数", "询价累计报价倍数", "配售对象报价家数", 
            "上市日期", "上市10日后最高涨幅"
        ]
        
        # Filter existing columns
        existing_cols = [c for c in desired_cols if c in df.columns]
        df_to_save = df[existing_cols]
        
        df_to_save.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Data saved to {output_path}")
        
        # Display sample
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        # Show rows where Listing Date is not null to verify logic
        if "上市日期" in df.columns:
            print(df_to_save[df_to_save['上市日期'].notna()].head())
