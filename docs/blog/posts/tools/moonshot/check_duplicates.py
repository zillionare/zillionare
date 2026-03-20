# 检查并显示重复的MultiIndex行

def check_duplicate_indices(consective_flag):
    """
    检查并显示consective_flag中的重复索引项
    
    Args:
        consective_flag: 包含MultiIndex的DataFrame
    """
    print("检查重复索引项...")
    
    # 检查是否有重复索引
    if consective_flag.index.duplicated().any():
        print(f"发现 {consective_flag.index.duplicated().sum()} 个重复索引项")
        
        # 获取重复索引的布尔掩码
        dup_mask = consective_flag.index.duplicated(keep=False)
        
        # 显示所有重复的行（包括第一次出现的）
        print("\n重复的索引项及对应的数据：")
        duplicated_rows = consective_flag[dup_mask]
        print(duplicated_rows)
        
        # 按索引分组，显示每组重复项
        print("\n按索引分组显示重复项：")
        for idx, group in duplicated_rows.groupby(level=[0, 1]):
            print(f"\n索引 {idx} 有 {len(group)} 个重复项：")
            print(group)
            
        # 获取重复索引的唯一值
        duplicate_indices = consective_flag.index[consective_flag.index.duplicated()].unique()
        print(f"\n重复的唯一索引值：\n{duplicate_indices}")
        
        return True
    else:
        print("没有发现重复索引项")
        return False

# 使用示例：
# check_duplicate_indices(consective_flag)

# 更详细的检查函数，包括原始数据的分析
def analyze_duplicate_sources(dividend_data):
    """
    分析原始数据中可能导致重复索引的原因
    
    Args:
        dividend_data: 原始分红数据
    """
    print("\n分析原始数据中可能导致重复索引的原因...")
    
    # 检查原始数据中是否有重复的(asset, month)组合
    if 'asset' in dividend_data.columns and 'ann_date' in dividend_data.columns:
        # 创建月份列
        dividend_copy = dividend_data.copy()
        dividend_copy['month'] = pd.to_datetime(dividend_copy['ann_date']).dt.to_period('M')
        
        # 检查重复的(asset, month)组合
        dup_combinations = dividend_copy.duplicated(subset=['asset', 'month'])
        if dup_combinations.any():
            print(f"原始数据中发现 {dup_combinations.sum()} 个重复的(asset, month)组合")
            
            # 显示重复的组合
            print("\n重复的(asset, month)组合：")
            duplicated_combos = dividend_copy[dup_combinations][['asset', 'month', 'ann_date', 'fiscal_year']]
            print(duplicated_combos)
            
            # 按组合分组显示
            for (asset, month), group in duplicated_combos.groupby(['asset', 'month']):
                print(f"\n资产 {asset} 在 {month} 有 {len(group)} 条记录：")
                print(group[['ann_date', 'fiscal_year']])
        else:
            print("原始数据中没有重复的(asset, month)组合")
    
    # 检查预处理后是否有重复
    print("\n检查预处理过程...")
    
    # 模拟预处理过程
    dividend_processed = dividend_data.copy()
    dividend_processed["end_date"] = pd.to_datetime(dividend_processed["end_date"])
    dividend_processed["ann_date"] = pd.to_datetime(dividend_processed["ann_date"])
    dividend_processed["fiscal_year"] = dividend_processed["end_date"].dt.year
    dividend_processed["month"] = dividend_processed["ann_date"].dt.to_period("M")
    
    # 某些个股在一个财年，可能会有多次分红，我们取最早的一次
    dividend_dedup = (
        dividend_processed.sort_values(["asset", "fiscal_year", "ann_date"])
        .groupby(["asset", "fiscal_year"], as_index=False)
        .first()
    )
    
    # 检查去重后是否还有重复的(asset, month)组合
    dup_after_dedup = dividend_dedup.duplicated(subset=['asset', 'month'])
    if dup_after_dedup.any():
        print(f"去重后仍有 {dup_after_dedup.sum()} 个重复的(asset, month)组合")
        print("\n去重后重复的组合：")
        print(dividend_dedup[dup_after_dedup][['asset', 'month', 'ann_date', 'fiscal_year']])
    else:
        print("去重后没有重复的(asset, month)组合")

# 完整的检查流程
def full_duplicate_check(consective_flag, dividend_data=None):
    """
    完整的重复索引检查流程
    
    Args:
        consective_flag: 包含MultiIndex的DataFrame
        dividend_data: 原始分红数据（可选）
    """
    # 检查consective_flag中的重复索引
    has_duplicates = check_duplicate_indices(consective_flag)
    
    # 如果提供了原始数据，分析重复来源
    if dividend_data is not None:
        analyze_duplicate_sources(dividend_data)
    
    return has_duplicates

# 使用示例：
# full_duplicate_check(consective_flag, dividend_data)
