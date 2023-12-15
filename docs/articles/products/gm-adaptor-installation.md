【目录】

- [1.1. 安装](#11-安装)
- [1.2. 申请权限](#12-申请权限)
- [1.3. 模拟和测试](#13-模拟和测试)
  - [1.3.1. 配置账号](#131-配置账号)
    - [1.3.1.1. gmadaptor的配置文件](#1311-gmadaptor的配置文件)
    - [1.3.1.2. 配置EMC](#1312-配置emc)
  - [1.3.2. 模拟运行](#132-模拟运行)
- [1.4. 运行和维护](#14-运行和维护)
  - [1.4.1. 启动](#141-启动)
  - [1.4.2. 每日维护](#142-每日维护)
- [2.1. 客户端请求](#21-客户端请求)
- [2.2. 返回结果](#22-返回结果)
- [2.3. 资产表](#23-资产表)
- [2.4. 持仓表](#24-持仓表)
- [2.5. 限价买入](#25-限价买入)
- [2.6. 市价买入](#26-市价买入)
- [2.7. 限价卖出](#27-限价卖出)
- [2.8. 市价卖出](#28-市价卖出)
- [2.9. 取消委托](#29-取消委托)
- [2.10. 查询当日委托](#210-查询当日委托)
- [撮合配置规则](#撮合配置规则)
- [联系方式](#联系方式)

# 1. 安装与配置
## 1.1. 安装
1. 在windows机器上安装[https://emt.eastmoneysec.com/down](https://emt.eastmoneysec.com/down)，下载并安装第二个软件：
![](https://images.jieyu.ai/images/2023/03/20230403154605.png)

2. 在同一台机器上安装conda，推荐安装miniconda，并创建虚拟运行环境（python版本3.8）：
   ```
   conda create -n gmclient python=3.8
   ```
3. 安装gmadaptor:
    ```
    pip install gmadaptor-1.1.3-py3-none-any.whl
    ```
## 1.2. 申请权限
请加入东方财富量化仿真交流群：971584613 ，找管理员申请开通量化实盘权限。请先看群置顶文件。
开通的主要门槛是要求100万初始资金。开通后可以撤资。

## 1.3. 模拟和测试
在等待实盘权限开通的过程中，可以通过 https://emt.18.cn/apply/test-apply-client 开通模拟账号，先把程序和配置调通。

申请后，记录普通资金账号和密码，如下图：

![](https://images.jieyu.ai/images/2023/04/仿真.jpg)

在登录界面中，选择仿真交易：

![](https://images.jieyu.ai/images/2023/04/login.jpg)

登录后，界面显示如下：

![](https://images.jieyu.ai/images/2023/04/20230403200024.png)

### 1.3.1. 配置账号
以下步骤对实盘和模拟盘均有效。

#### 1.3.1.1. gmadaptor的配置文件
需要将量化软件中的实盘账号配置到gmadaptor的配置文件中。在用户目录下，创建`gmadaptor/config`目录，放置以下文件：
```yaml
# defaults.yaml
log_level: INFO

server_info:
    port: 9000
    # client 使用这一token来访问 gmadaptor 提供的服务
    access_token : "84ae0899-7a8d-44ff-9983-4fa7cbbc424b"

gm_info:
    fake: false
    # 文件单输出目录
    gm_output: "~/gmadaptor/FileOrders/out"
    trade_fees:
        commission: 2.5
        stamp_duty: 10.0
        transfer_fee: 0.1
        minimum_cost: 5.0
    accounts:
        # 账号名
        - name: fileorder_s01
          acct_id: 1a66e81c-ae5d-11ec-aef5-00163e0a4100
          # 文件单输入目录。东财量化终端将从这里读取文件单
          acct_input: "~/gmadaptor/FileOrders/inputs/fileorder_s01"
```
上述配置中，access_token 可任意指定，任何要访问此服务的客户端，必须持有此 token。

gm_output/acct_input 文件设置后，如果未创建，gmadaptor 将在启动时自动创建，请确保 gmadaptor 有权限读写这些文件夹。

accounts > name 中的值来自于在 EMC 终端中，您创建文件单输入时，指定的名称，见下图中的序号2：

![](https://images.jieyu.ai/images/2023/04/20230403194653.png)

accounts > acct_id 来自于下面序号3的位置，点击`ID`即可复制：

![](https://images.jieyu.ai/images/2023/04/20230403195425.png)

#### 1.3.1.2. 配置EMC

在 量化 > 文件单 > 文件单输出 中，对下图中的 4，5，6，7 进行配置。其中4选择我们在上面配置文件中gm_output中设置的路径；5选择`csv`作为输出格式；6选择自动启动；7将所有项目全选中。

![](https://images.jieyu.ai/images/2023/04/output.jpg?1)

在 量化 > 文件单 > 文件单输入 中，对下图中的 3和4进行配置。其中3选择我们在上面配置文件中设置的 acct_input 路径，4选择自动启动。

![](https://images.jieyu.ai/images/2023/04/input.jpg?1)


### 1.3.2. 模拟运行

在前面生成的gmclient虚拟环境中，执行以下命令，以启动gmadaptor服务器：
```
python -m gmadaptor.server
```
如果出现如下界面，表明服务器启动成功：

![](https://images.jieyu.ai/images/2023/04/started.jpg)

此时我们另开一个`conda`窗口，同样使用`gmclient`的虚拟环境，通过以下命令进行测试:
```
python -m gmtest %account %token %server %port
```

这里的account即 gmadaptor配置文件中的 gm_info > accounts > account_id, token 即server_info > access_token

这里的 server 即gmadaptor 所在的机器IP， port为端口。如果不提供，默认地，这两项分别为localhost和9000。

如果配置正常，这将打印出初始账号资金，当前持仓，和一笔买、卖的信息。
## 1.4. 运行和维护

另外启动一个计划任务，在每天早上8:45左右启动EMC。
### 1.4.1. 启动
使用下面的脚本来启动：
```
@echo off
call C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\anaconda3
call conda activate gmclient
python -m gmadaptor.server
pause
```

### 1.4.2. 每日维护
EMC量化终端有时候不稳定。我们可以通过定时重启来提高起稳定性。通过以下代码，在盘后退出EMC：
```
REM kill process
TASKKILL /F /IM EMCTrade.exe

REM sleep 5 seconds
TIMEOUT  /T 5

REM remove all file orders after process killed

DEL /Q C:\zillionare\FileOrders\real_input\*.csv
```

!!! Warning
    如果在输入输出目录中还有未归档的文件，则量化交易将无法自动启动。上述代码中最后一行的作用就是清理未归档文件。
    这也要求使用者自行对委托进行核验，确保这些文件可以被自动删除。
# 2. 客户端与服务器交互
## 2.1. 客户端请求

客户端通过 http request来请求gmadaptor。以下示例均以同步请求实现，但您也可以根据需要，改为异步请求。服务器对客户端的鉴权是通过`headers`来实现的，具体请看示例（任意一示例均可）。客户端向服务器发送数据，都使用的是post方法，gmadaptor所有的方法都只响应post请求。如果请求成功完成，则返回代码是200。

在所有的操作中，股票代码都必须以简码+交易所后缀方式出现，其中上交所为.XSHG，深交所为.XSHE。在仿真测试时，对股票进行操作时，都有特定的响应（比如对某支股票，进行买入时，无论给的参数是多少，返回都会是部分成交；对另一支股票，则永远返回限制买入等等），具体响应文档请在东财量化Q群中，找管理员要文档。

在一些会改变状态的请求中（比如买入操作），往往会需要`cid`参数和`timeout`参数，其作用是，调用会在指定的timeout期间等待EMC处理请求，并返回结果；但EMC也可能无法在指定的timeout期间返回结果，比如委买单报价过低，一直不能成交，此时将无法产生回报结果。在这种情况下，调用会在timeout之后返回。之后的委买结果查询，就需要依赖`cid`参数。注意`cid`是必选参数，`timeout`是可选参数。

`cid`参数（即client entrust id）由客户端自行产生，建议使用以下代码：
```python
import uuid

cid = str(uuid.uuid4())
```
`cid`产生之后，请在客户端保存，直到事务结束，不再需要为止。

为简练起见，以下示例中，可能删除了这些代码：
```python
import httpx
headers = {
    "Authorization": "84ae0899-7a8d-44ff-9983-4fa7cbbc424b",
    "Account-ID": "780dc4fda3d0af8a2d3ab0279bfa48c9"
}

_url_prefix = "http://192.168.100.100:9000/"

buy_entrust_no = None
sell_entrust_no = None
```

## 2.2. 返回结果
返回错误可能发生在三个层面。一是http层（包括 bad request 或者 Internal server error); 二是 gmadaptor层，三是 emc可能返回错误。

第一层的错误，我们通过 http status code来检查。比如，如果我们使用的客户端是httpx，则可以检查 `response.status_code`是否为200。

gmadaptor始终通过`json`来返回响应，响应包括三个字段，即：
```
status: int,如果为零，则表明在此层没有发生错误，即gmadaptor已经将请求正确上报
msg: str, human readable message
data: dict 如果一切顺利，则返回数据在此项中
```
第三层的错误由 emc trader给出。即使gmadaptor正确上报的请求，也可能emc trader无法执行，此时它也会通过`status`和`reason`来给出错误信息。

下面的示例给出了一个`response.json()`的输出：
```json
{
    "status": 0,
    "msg": "OK",
    "data": {
        "code": "000001.XSHE",
        "price": 0.0,
        "volume": 100,
        "order_side": 1,
        "bid_type": 2,
        "time": "2023-04-04 15:27:38.921555",
        "entrust_no": "0d23bb4e-d81e-4ef2-ab21-c58e0fe6814f",
        "status": -1,
        "average_price": 0.0,
        "filled": 0,
        "filled_amount": 0,
        "eid": "",
        "trade_fees": 0,
        "reason": "[Counter] [EMC_PC]不支持该下单类型",
        "recv_at": "2023-04-04 15:27:38.924565"
    }
}
```
因此，即使在gmadator层面给出的状态是成功，也并不意味着该笔委托成功。另一个例子是，以过低的价格委买，只要参数合法且被EMC接收，gmadaptor都会返回成功，但该委托是否真正成交，还得通过entrust_no来查询。
## 2.3. 资产表
```python
# 请求资金信息
import httpx
headers = {
    "Authorization": "84ae0899-7a8d-44ff-9983-4fa7cbbc424b",
    "Account-ID": "780dc4fda3d0af8a2d3ab0279bfa48c9"
}

_url_prefix = "http://192.168.100.100:9000/"

def get_balance():
    r = httpx.post(_url_prefix + "balance", headers=headers)
    resp = r.json()
    if r.status_code == 200 and resp['status'] == 0:
        print("\n------ 账户资金信息 ------")
        print(resp["data"])
```

## 2.4. 持仓表
```python
def get_positions():
    r = httpx.post(_url_prefix + "positions", headers=headers)
    
    resp = r.json()
    if r.status_code == 200 and resp['status'] == 0:
        print("\n----- 持仓信息 ------")
        print(resp["data"])
```

## 2.5. 限价买入
```python
    r = httpx.post(_url_prefix + "buy", headers=headers, json={
        "security": "000001.XSHE",
        "price": 13,
        "volume": 100,
        "cid": str(uuid.uuid4()),
        "timeout": 1
    })

    print(r.json())
```

## 2.6. 市价买入
```python
def market_buy():
    global buy_entrust_no
    r = httpx.post(_url_prefix + "market_buy", headers=headers, json={
        "security": "000001.XSHE",
        "volume": 100,
        "cid": cid,
        "timeout": 1
    })

    resp = r.json()
    if r.status_code == 200 and resp["status"] == 0:
        print("\n ------ 委买成功 ------")
        print(resp["status"], resp["msg"], resp["data"])
        buy_entrust_no = resp["data"]["entrust_no"]
    else:
        print("委买失败:", r.status_code, resp)
```

## 2.7. 限价卖出
```python
def sell():
    global sell_entrust_no

    r = httpx.post(_url_prefix + "sell", headers=headers, json={
        "security": "000001.XSHE",
        "price": 10,
        "volume": 100,
        "cid": cid,
        "timeout": 1
    })

    resp = r.json()
    if r.status_code == 200 and resp["status"] == 0:
        print("\n ------ 限价委卖成功 ------")
        data = resp["data"]
        print(data)
        sell_entrust_no = data["entrust_no"]
    else:
        print("卖出失败:", r.status_code, resp)
```

## 2.8. 市价卖出
```python
def market_sell():
    r = httpx.post(_url_prefix + "market_sell", headers=headers, json = {
        "security": "000001.XSHE",
        "volume": 100,
        "cid": cid
    })

    resp = r.json()
    if r.status_code == 200 and resp["status"] == 0:
        print("\n ------ 市价委卖成功 ------")
        print(resp["data"])
    else:
        print(resp)
```
## 2.9. 取消委托
```python
def cancel_entrust():
    global buy_entrust_no

    r = httpx.post(_url_prefix + "cancel_entrust", headers=headers, json = {
        "entrust_no": buy_entrust_no,
        "timeout": 1
    })

    resp = r.json()
    print(resp["status"], resp["msg"], resp["data"])

```
## 2.10. 查询当日委托
```python
def today_entrusts():
    r = httpx.post(_url_prefix + "today_entrusts", headers=headers, json = {
        # 此处可以传入记录的委托号。传入空数组时，表明取当天所有委托。
        "entrust_no": [],
        "timeout": 1
    })

    resp = r.json()
    print(resp["status"], resp["msg"], resp["data"])
```

# 3. 故障排除与帮助

关于东财文件单，请参考：https://emquant.18.cn/file-help/?doc=file_order
东财量化Q群：971584613

即使实现了EMC的每日自动重启，也有可能偶发连接异常或者其它错误。此时可能需要手动执行：
1. 重新连接
2. 清除文件单，重新启动

## 撮合配置规则
在仿真交易测试中，EMTrader对每个品种，都指定了对应的响应。比如，对000572这个品种，买入一定会全部成交，对000010这个品种，则一定会拒绝。这是为了方便测试的需要。东财提供了名为《撮合配置规则》的文件，该文件可能随时更新，所以，需要在测试前，加他们技术人员QQ领取。

该文件2023年3月份部分内容如下：
```
[全部成交]
000572	full
000725	full

[分笔成交] 
分成两笔：
000002	lot      	2

[部分成交] 成交一半
000001	part
000004	part
...
[挂单]	只有响应，没有成交
018014	pending
020417	pending
...

[拒单]	
000010	reject
010609	reject

[拒绝撤单] 部分成交，不可撤单
000008	cancel_reject
000151	cancel_reject
```

## 联系方式

如果您在使用本模块中需要帮助，或者需要参加[《大富翁量化编程实战课》](https://github.com/zillionare)学习，请添加 宽粉 的微信：

![](https://images.jieyu.ai/images/hot/quantfans.jpg)

