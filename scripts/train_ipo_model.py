import datetime
import os
import warnings

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split

# Suppress warnings
warnings.filterwarnings('ignore')

def train_model(start: datetime.date = None):
    # 1. Load Data
    file_path = os.path.join(os.path.dirname(__file__), 'ipo_data.csv')
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)

    # 2. Preprocessing
    # Filter out rows with missing target
    if start is not None:
        df = df.query(f"上市日期 >= '{start.isoformat()}'")
    df = df.dropna(subset=['上市10日后最高涨幅'])
    print(f"Data size after dropping missing targets: {len(df)}")

    # Ensure numeric columns are actually numeric
    numeric_cols_raw = [
        '发行总数', '网上发行股数', '总股本', '顶格申购需配市值', '申购上限', 
        '发行价格', '行业市盈率', '净利润', '净资产',
        '网上有效申购倍数', '询价累计报价倍数', '配售对象报价家数'
    ]
    
    for col in numeric_cols_raw:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Reconstruct Issue PE if missing or empty
    # Issue PE = Issue Price / (Net Profit / Total Shares)
    if '发行市盈率' not in df.columns or df['发行市盈率'].isnull().all():
        print("Reconstructing '发行市盈率' (Issue PE)...")
        # Avoid division by zero
        df['calculated_eps'] = df['净利润'] / df['总股本']
        df['发行市盈率'] = df.apply(
            lambda row: row['发行价格'] / row['calculated_eps'] if row['calculated_eps'] > 0 else np.nan, 
            axis=1
        )
    else:
        df['发行市盈率'] = pd.to_numeric(df['发行市盈率'], errors='coerce')

    # Calculate Valuation Difference
    if '估值差' not in df.columns or df['估值差'].isnull().all():
        if '行业市盈率' in df.columns and '发行市盈率' in df.columns:
            print("Calculating '估值差' (Valuation Difference)...")
            df['估值差'] = df['行业市盈率'] - df['发行市盈率']

    # --- New Feature: Market Regime (Past IPO Performance) ---
    print("Calculating Market Regime features (1w, 1m, 3m)...")
    if '上市日期' in df.columns and '上市10日后最高涨幅' in df.columns:
        df['上市日期'] = pd.to_datetime(df['上市日期'], errors='coerce')
        
        # Sort by date to ensure chronological order (helper for debugging, not strictly needed for logic)
        df = df.sort_values('上市日期').reset_index(drop=True)
        
        # Define lookback windows in days
        windows = {
            'market_regime_1w': 7,
            'market_regime_1m': 30,
            'market_regime_3m': 90
        }
        
        # Prepare arrays for faster iteration
        dates = df['上市日期'].values
        targets = df['上市10日后最高涨幅'].values
        
        # Dictionary to store results
        new_features = {k: np.full(len(df), np.nan) for k in windows.keys()}
        
        for i in range(len(df)):
            current_date = dates[i]
            if pd.isnull(current_date):
                continue
                
            for feat_name, days in windows.items():
                cutoff_date = current_date - np.timedelta64(days, 'D')
                
                # Filter: listed within [current_date - days, current_date)
                # strictly less than current_date to avoid data leakage
                mask = (dates >= cutoff_date) & (dates < current_date)
                
                # Only calculate if we have samples
                if np.any(mask):
                    # Ignore NaNs in the target when calculating mean
                    vals = targets[mask]
                    valid_vals = vals[~np.isnan(vals)]
                    if len(valid_vals) > 0:
                        new_features[feat_name][i] = np.mean(valid_vals)
        
        # Add to DataFrame
        for k, v in new_features.items():
            df[k] = v

    # Log transform for strictly positive skewed features
    # We create NEW columns for these to let the model choose
    log_candidates = [
        '发行总数', '网上发行股数', '总股本', '顶格申购需配市值', '申购上限', 
        '发行价格', '行业市盈率', '发行市盈率', 
        '网上有效申购倍数', '询价累计报价倍数', '配售对象报价家数'
    ]

    for col in log_candidates:
        if col in df.columns:
            # Create a new feature with log prefix
            # Use log1p to handle zeros/small numbers
            # We filter for > 0 to avoid errors
            df[f'log_{col}'] = df[col].apply(lambda x: np.log1p(x) if pd.notnull(x) and x > 0 else np.nan)

    # Categorical Features
    cat_cols = ['上市板块', '所属行业', '保荐机构']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')

    # Select Features
    # Exclude non-predictive or target columns
    exclude_cols = ['股票代码', '股票简称', '上市日期', '上市10日后最高涨幅', 'calculated_eps']
    
    # We use all remaining columns as features
    feature_cols = [c for c in df.columns if c not in exclude_cols]
    
    X = df[feature_cols]
    y = df['上市10日后最高涨幅']
    
    print(f"Training with {len(feature_cols)} features.")
    
    # Split for final evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Model Training with Hyperparameter Tuning
    # Define search space
    param_dist = {
        'num_leaves': [31, 50, 70, 100],
        'max_depth': [-1, 10, 20, 30],
        'learning_rate': [0.02, 0.05, 0.1],
        'n_estimators': [50, 100, 200],
        'min_child_samples': [10, 20, 30, 50],
        'subsample': [0.5, 0.7, 0.8],
        'colsample_bytree': [0.5, 0.7, 0.8],
        'reg_alpha': [0.1, 0.5, 1.0],
        'reg_lambda': [0.0, 0.1, 0.5]
    }

    lgbm = lgb.LGBMRegressor(random_state=42, verbose=-1)

    search = RandomizedSearchCV(
        lgbm, 
        param_distributions=param_dist, 
        n_iter=50,  # Try 50 combinations
        scoring='neg_mean_absolute_error', 
        cv=5, 
        random_state=42,
        n_jobs=-1,
        verbose=0
    )

    print("Starting hyperparameter tuning (RandomizedSearchCV)...")
    search.fit(X_train, y_train)

    best_model = search.best_estimator_
    print(f"Best params: {search.best_params_}")

    # 4. Evaluation
    y_pred = best_model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("-" * 30)
    print(f"Test MAE: {mae:.4f}")
    print(f"Test R2: {r2:.4f}")
    print("-" * 30)

    # 5. Show 5 test cases
    print("\nTop 5 Test Cases (Actual vs Predicted):")
    # Reset index of X_test and y_test to allow easy integer indexing for display
    # But we need original indices to look up stock codes
    
    # Let's take first 5 from the test set
    sample_indices = y_test.index[:5]
    
    for idx in sample_indices:
        actual = y_test.loc[idx]
        # Predict expects a DataFrame
        predicted = best_model.predict(X.loc[[idx]])[0]
        
        stock_code = df.loc[idx, '股票代码']
        stock_name = df.loc[idx, '股票简称']
        
        print(f"Code: {stock_code}, Name: {stock_name}")
        print(f"  Actual: {actual:.4f} ({actual*100:.2f}%)")
        print(f"  Pred  : {predicted:.4f} ({predicted*100:.2f}%)")
        print(f"  Diff  : {predicted-actual:.4f}")
        print("-" * 20)

    # Feature Importance
    print("\nTop 20 Feature Importances:")
    importances = pd.DataFrame({
        'feature': feature_cols,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(importances.head(20))

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        start = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        train_model(start)
    else:
        train_model()
