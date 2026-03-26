---
title: 如何利用审计意见
---

4. 审计意见。只有过去十年没有审计保留意见的公司才能入选。<!--pro.audit-->
5. 市值数据。只有市值大于 50 亿的公司才能入选。 <!-- pro.daily_basic -->
6. 净利润、营业收入和营业利润数据，用来计算净利润稳定性因子。<!-- pro.income -->
7. 股东数量变化 <!-- pro.stk_holdernumber -->
8. 换手率。用来计算换手波动率。<!-- pro.daily_basic -->
9. pe_ttm，用来计算 ep 因子。
10. 经营现金流数据，用来计算经营现金流资产比因子。<!-- pro.cashflow_vip.n_cashflow_act-->
11. 资产总计数据，与 10 一起，用来计算经营现金流资产比因子。 <!-- pro.balancesheet_vip.total_assets -->
12. 盈余公积金数据。与 11 一起，用来计算留存收益资产比因子。<!-- pro.balancesheet_vip.surplus_rese -->

## 什么是审计意见

在 tushare 中，获取审计意见的 API 是 fina_audit。这个API 的方法签名是：

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/09/20250922183044.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

它将返回一个 DataFrame，包含以下字段：

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/09/20250922183213.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>fina_audit 返回字段及示例</span>
</div>


我们需要对字段如何使用进行一些解释。与之前一样，end_date 仍然是对应财年的结束日。因此，20181231表明该条记录对应的是2018年的审计意见。

ann_date 则是公告日期。从图中可以看出，2018年的审计意见是2019年4月10日出具的。

audit_result 是审计结果，尽管它是文本字段，但只能取这样几个字面量：

* 标准无保留意见。表明公司的财报完全公允，无重大错报。
* 带强调事项段的无保留意见。整体公允，但需关注特定风险事项。比如，2023年4月29日，中兴华就对002104出具了这种审计意见。
* 保留意见。局部不公允 / 证据不足，整体尚可。比如，2021年4月30日，四川华信就对600311出具了此类意见。
* 否定意见。整体不公允，存在严重错报	
* 无法表示意见。无法判断报表是否公允（证据不足）

我们做基本面量化时，一般只在第一种中构建资产池；后面几种一般都要排除掉。

!!! attention
    即使审计机构出具了标准无保留意见，我们也不能完全排除该公司的财务数据存在错误。你可以通过`df["audit_agency"].unique()`把事务所提取出来，然后通过豆包查询，哪些事务所卷入过腐败或者违规案件，你会得到一个不算很短的清单。

其它字段在我们的策略中，不太关心，因此就不介绍了。对它们深入研究，可以得到一些另类数据，但要注意这些数据很容易产生未来信息。

## 获取审计意见

根据 tushare 的 api文档，资产代码是必选参数，因此，我们必须先构造一个资产列表，再对其进行遍历，这样才能得到全部的资产审计意见。

我们可以简单地使用 daily_basic 来最新的资产列表：

```python
import tushare as ts

pro = ts.pro_api()

df = pro.daily_basic()
securities = df["ts_code"].tolist()
```

然后，我们可以遍历这个列表，获取每个资产的审计意见：

```python
import time
dfs = []

start = datetime.date(2018, 1, 1)
end = datetime.date(2023, 12, 31)
for i, sec in enumerate(securities):
    df = pro.fina_audit(ts_code = sec, 
                        start_date = start.strftime("%Y%m%d"), 
                        end_date=end.strftime("%Y%m%d"))
    if not df.empty:
        dfs.append(df)

    time.sleep(0.125)
    if i % 500 == 0:
        print(f"processed {i} securities")

audit_report = pd.concat(dfs, axis=0)
audit_report.head()
```

这个过程非常耗时。即使我们去掉`time.sleep(0.125)`，执行时间也超过了30分钟。所以，如果要使用这项数据，你最好得提前规划，并且建立缓存。

以下是如何使用我们之前定义的 parquet 缓存的简单实现。为节省篇幅，这里从略，你可以在我们的星球中找到完整代码。

```python
from helper import ParquetUnifiedStorage 

def fetch_fina_audit(start: datetime.date, end: datetime.date) -> pd.DataFrame | None:
    """
    通过 tushare 接口，获取财务审计意见数据。

    Args:
        start: 开始日期 (基于公告日期 ann_date)
        end: 结束日期 (基于公告日期 ann_date)

    Returns:
        DataFrame: 包含审计意见等数据的DataFrame
    """
    pro = ts.pro_api()
    
    # Tushare API 使用 'YYYYMMDD' 格式的字符串作为日期参数
    start_str = start.strftime('%Y%m%d')
    end_str = end.strftime('%Y%m%d')
    
    try:
        # 一次性获取指定日期范围内所有股票的审计数据
        df = pro.fina_audit(start_date=start_str, end_date=end_str)
        
        if df.empty:
            return None

        # --- 数据清洗和标准化 ---
        # 1. 为了兼容 ParquetUnifiedStorage，重命名关键列
        #    'ann_date' 作为时间索引，'ts_code' 作为资产标识
        df = df.rename(columns={'ann_date': 'date', 'ts_code': 'asset'})

        # 2. 将字符串日期转换为 datetime.date 类型
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d').dt.date
        
        # 3. 选择需要的列（可选，但推荐）
        #    这里保留了所有列，您可以根据需要进行筛选
        #    cols_to_keep = ['date', 'asset', 'audit_result', 'audit_fees', 'audit_agency']
        #    df = df[cols_to_keep]

        return df

    except Exception as e:
        print(f"获取审计数据时发生错误: {e}")
        return None
```
