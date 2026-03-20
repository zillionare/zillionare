ESG 数据定义请参考:

https://finance.sina.com.cn/esg/grade.shtml


```python
import akshare as ak
print("akshare version is ", ak.__version__)
```


## MSCI 评级数据


```python
# ESG MSCI 评级

esg_msci = ak.stock_esg_msci_sina()
print(f"总记录数: {len(esg_msci)}")
esg_msci.head()
```

## 标普

缺

## 路孚特


```python
# 路孚特评级，该接口只能获取100条记录；需要自己重新实现。或者换一个更新的 akshare 版本
esg_rft = ak.stock_esg_rft_sina()
print(f"总记录数: {len(esg_rft)}")
esg_rft.head()
```


## 中证
缺

## ESG 评级数据，含多家评级机构


```python
# ESG 评级数据，含多家评级机构

esg_rate = ak.stock_esg_rate_sina()
print(f"总记录数: {len(esg_rate)}")
esg_rate.head()
```

## 秩鼎评级


```python
df_zd = ak.stock_esg_zd_sina()
print(f"总记录数: {len(df_zd)}")
df_zd.head()
```

## ESG 华证指数


```python
esg_hz = ak.stock_esg_hz_sina()
print(f"总记录数: {len(esg_hz)}")
esg_hz.head()
```
