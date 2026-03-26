# dividend接口的隐藏参数

### 分红数据

在 tushare 中获取分红数据，要通过通过 pro.dividend 这个 API。使用它要求有2000积分以上。该函数的签名是：

```
{code-block}python
dividend(
    ts_code: str = '',
    ann_date: str = '',
    record_date: str = '',
    ex_date: str = '',
    imp_ann_date: str = ''
)
```

尽管这些参数都声明为可选参数，但是，必须至少提供一个以上。有意思的是，根据它的输出，我们发现它还有一个隐藏的 end_date 参数。这个参数有何作用呢？

下面是我们使用不同参数，进行的比较：

```python
# example-1
pro = pro_api()

df_ann = pro.dividend(ann_date="20250419")
print("by ann_date", len(df_ann))

df_end = pro.dividend(end_date="20241231")
print("by end_date", len(df_end))

df_ex = pro.dividend(ex_date="20250419")
print("by ex_date", len(df_ex))

df_record = pro.dividend(record_date="20250419")
print("by record_date", len(df_record))

df_imp = pro.dividend(imp_ann_date="20250419")
print("by imp_ann_date", len(df_imp))
```


我们得到的输出如下：

<!-- BEGIN IPYNB STRIPOUT -->
```md
by ann_date 647
by end_date 2000
by ex_date 0
by record_date 0
by imp_ann_date 4
```
<!-- END IPYNB STRIPOUT -->


通过 end_date 参数，我们可以一次下载2000条记录，是所有下载方式中，一次可获取记录数最多的，加速比可达15倍！但是，这个非公开的参数，要如何使用呢？

事实上，截止2025年为止，A 股共有约5400支个股。按照规定，它们都必须批露年报，并对是否进行送转和分红做出决定。因此，以20241231为分红年度（即 end_date == '20241231'）的记录至少有5400条。而上述运行结果只显示了2000条。是否存在剩下的记录？又该如何获取它们？

经过我们试验，可以通过以下方法来获取所有记录：

```python
# example-2
dfs = []
for offset in range(0, 99):
    df = pro.dividend(end_date="20241231", offset=offset * 2000, pagesize=2000)
    dfs.append(df)
    if len(df) < 2000:
        break

df_end_all = pd.concat(dfs)
df_end_all
```

现在，我们要验证通过这个 undocumented 的参数，得到的结果是否与通过其它参数得到的结果一致。在 example-1 中，看起来获取数据最快的方式是通过 ann_date(理论上，通过其它参数也应该一样)。于是，我们通过下面的代码，从另一个角度获取2024年的分红数据：

```python
# example-3
start = datetime.date(2025, 1, 1)
end = datetime.date(2025, 4, 30)
dates = pd.date_range(start, end)

dfs = []
for date in dates:
    df = pro.dividend(ann_date = date.strftime('%Y%m%d'))
    dfs.append(df)

df_ann_all = pd.concat(dfs)
df_ann_all
```

毫不奇怪，我们得到的 df_end_all 与 df_ann_all 在记录数上大致相当，但仍有许多不同之处。我们以 ts_code 和 end_date 作为索引，来检查下它们不同在何处。这种差异也揭示了基本面数据清选难在何处。


```python
set1 = set(df_end_all.set_index(["ts_code", "end_date"]).index)
set2 = set(df_ann_all.set_index(["ts_code", "end_date"]).index)

# df_end_all - df_ann_all
(df_end_all.set_index(["ts_code", "end_date"])).loc[list(set1 - set2)]
```

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250814152151.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

这个结果表明，有一些个股，它们的分红方案会出得很晚，比如600777这支，去年的分红方案直到今年的7月5日才宣布。另一方面，去年三季度的分红方案，也可能拖到今年才宣布；或者在4月份，就宣布了一季度的分红方案。我们通过下面的代码可以找出这些情况：

```python
df_all.set_index(["ts_code", "end_date"]).loc[list(set2 - set1)]
```


<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250814153358.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

!!! tip
    我们提供了两种以上的方法来获得分红数据，实战中究竟应该使用哪一个呢？尽管通过 end_date 参数在速度上会快很多，但我们仍然建议使用官方文档中的参数，比如 ann_date。毕竟 end_date 参数的 undocumented 的属性，让我们担心，长期使用它会不会不太可靠。但是，当你使用 ann_date 时，也要注意，你可能得往后面取很久，才能取全上个年度的数据。

    从分红送股信息批露的情况来看，做基本面量化确实有它的难处：数据到达的时间差异很大。无论是回测还是实盘，这都容易引起一些问题。比如，在2025年1月份25日，就已经有了7支个股批露了上年度的分红方案。但是，此时由于拿不到其它个股的分红数据，如果我们的策略是基于横截面的，该如何实施呢？



我们已经得到了分红数据。这里我们关心的有 ts_code, end_date， ann_date，以及 cash_div_tax 等列。考虑到事件信息的时间衰减效应，一般来说，我们不必对 record_date, ex_date 和 pay_date，imp_ann_date 感兴趣。它们都出现在 ann_date 之后。

现在，我们要如何得到股息率数据呢？从公式上看，只要用分红除以每股市价，就可以得到股息率。但是，应该使用哪一天的市价？

## 股息率的计算
### 分红数据

在 tushare 中获取分红数据，要通过通过 pro.dividend 这个 API。使用它要求有2000积分以上。该函数的签名是：

```{code-block}python
dividend(
    ts_code: str = '',
    ann_date: str = '',
    record_date: str = '',
    ex_date: str = '',
    imp_ann_date: str = ''
)
```

尽管这些参数都声明为可选参数，但是，必须至少提供一个以上。有意思的是，根据它的输出，我们发现它还有一个隐藏的 end_date 参数。这个参数有何作用呢？

下面是我们使用不同参数，进行的比较：

```python
# example-1
pro = pro_api()

df_ann = pro.dividend(ann_date="20250419")
print("by ann_date", len(df_ann))

df_end = pro.dividend(end_date="20241231")
print("by end_date", len(df_end))

df_ex = pro.dividend(ex_date="20250419")
print("by ex_date", len(df_ex))

df_record = pro.dividend(record_date="20250419")
print("by record_date", len(df_record))

df_imp = pro.dividend(imp_ann_date="20250419")
print("by imp_ann_date", len(df_imp))
```


我们得到的输出如下：

<!-- BEGIN IPYNB STRIPOUT -->
```md
by ann_date 647
by end_date 2000
by ex_date 0
by record_date 0
by imp_ann_date 4
```
<!-- END IPYNB STRIPOUT -->


通过 end_date 参数，我们可以一次下载2000条记录，是所有下载方式中，一次可获取记录数最多的，加速比可达15倍！但是，这个非公开的参数，要如何使用呢？

事实上，截止2025年为止，A 股共有约5400支个股。按照规定，它们都必须批露年报，并对是否进行送转和分红做出决定。因此，以20241231为分红年度（即 end_date == '20241231'）的记录至少有5400条。而上述运行结果只显示了2000条。是否存在剩下的记录？又该如何获取它们？

经过我们试验，可以通过以下方法来获取所有记录：

```python
# example-2
dfs = []
for offset in range(0, 99):
    df = pro.dividend(end_date="20241231", offset=offset * 2000, pagesize=2000)
    dfs.append(df)
    if len(df) < 2000:
        break

df_end_all = pd.concat(dfs)
df_end_all
```

现在，我们要验证通过这个 undocumented 的参数，得到的结果是否与通过其它参数得到的结果一致。在 example-1 中，看起来获取数据最快的方式是通过 ann_date(理论上，通过其它参数也应该一样)。于是，我们通过下面的代码，从另一个角度获取2024年的分红数据：

```python
# example-3
start = datetime.date(2025, 1, 1)
end = datetime.date(2025, 4, 30)
dates = pd.date_range(start, end)

dfs = []
for date in dates:
    df = pro.dividend(ann_date = date.strftime('%Y%m%d'))
    dfs.append(df)

df_ann_all = pd.concat(dfs)
df_ann_all
```

毫不奇怪，我们得到的 df_end_all 与 df_ann_all 在记录数上大致相当，但仍有许多不同之处。我们以 ts_code 和 end_date 作为索引，来检查下它们不同在何处。这种差异也揭示了基本面数据清选难在何处。


```python
set1 = set(df_end_all.set_index(["ts_code", "end_date"]).index)
set2 = set(df_ann_all.set_index(["ts_code", "end_date"]).index)

# df_end_all - df_ann_all
(df_end_all.set_index(["ts_code", "end_date"])).loc[list(set1 - set2)]
```

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250814152151.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

这个结果表明，有一些个股，它们的分红方案会出得很晚，比如600777这支，去年的分红方案直到今年的7月5日才宣布。另一方面，去年三季度的分红方案，也可能拖到今年才宣布；或者在4月份，就宣布了一季度的分红方案。我们通过下面的代码可以找出这些情况：

```python
df_all.set_index(["ts_code", "end_date"]).loc[list(set2 - set1)]
```


<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250814153358.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

!!! tip
    我们提供了两种以上的方法来获得分红数据，实战中究竟应该使用哪一个呢？尽管通过 end_date 参数在速度上会快很多，但我们仍然建议使用官方文档中的参数，比如 ann_date。毕竟 end_date 参数的 undocumented 的属性，让我们担心，长期使用它会不会不太可靠。但是，当你使用 ann_date 时，也要注意，你可能得往后面取很久，才能取全上个年度的数据。

    从分红送股信息批露的情况来看，做基本面量化确实有它的难处：数据到达的时间差异很大。无论是回测还是实盘，这都容易引起一些问题。比如，在2025年1月份25日，就已经有了7支个股批露了上年度的分红方案。但是，此时由于拿不到其它个股的分红数据，如果我们的策略是基于横截面的，该如何实施呢？



我们已经得到了分红数据。这里我们关心的有 ts_code, end_date， ann_date，以及 cash_div_tax 等列。考虑到事件信息的时间衰减效应，一般来说，我们不必对 record_date, ex_date 和 pay_date，imp_ann_date 感兴趣。它们都出现在 ann_date 之后。

现在，我们要如何得到股息率数据呢？从公式上看，只要用分红除以每股市价，就可以得到股息率。但是，应该使用哪一天的市价？

## 题外话之二： tushare 中的分页查询

