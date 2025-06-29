在scripts/data.py中，我们提供了数据访问方法load_bars和pro.

前者可以获得2023年底以前的A股日线行情数据。返回数据是pd.DataFrame，以date和asset为索引，列为open,high,low,close,volume,amount,factor,price.其中price是次日的开盘价。

pro即为tushare对象，相当于：

```python
import tushare as ts
ts.set_token('YOUR_TOKEN')
pro = ts.pro_api()
```

你可以直接使用这个对象，它已经初始化好了。

在本项目中，一般不用过多的错误处理、容错，它是面向读者的演示项目，过多的错误处理会增加阅读难度，并且没有必要。
