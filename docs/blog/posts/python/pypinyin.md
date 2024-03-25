---
title: 4k stars! 如何实现按拼音首字母查询证券代码？
slug: pypinyin-introduction
date: 2024-03-24
img: https://images.jieyu.ai/images/2024/03/pypinyin.png
categories:
    - python
motto:
lunar:
tags: 
    - quantlib
    - python
---

一个可能只有少数量化人才需要的功能 -- 按拼音首字母来查找证券。比如，当我们键入ZGPA时，就能搜索出中国平安，或者是它的代码。这是我们使用行情软件时常用的一个功能。

这个功能的关键是要实现汉字转拼音。有的数据源已经提供了这个查询。但不是所有的数据源都有这个功能。

---

如果我们使用的数据源是聚宽(jqdatasdk)，当我们调用jq.get_all_securities时，它返回的证券列表，将包括以下几项：

* index，证券代码代码，比如000001.XSHE
* display_name，证券的中文名，比如平安银行
* name，证券的拼音首字母名，比如PAYH
* start_date，证券IPO日
* end_date，该品种退市日。只有在已退市时，此时间才有效。
* type，证券类型，取值可能是stock, index, fund等。

我们要的关系反映在字段name与index, display_name中。当用户输入PAYH时，通过查找上述表格，就能找到对应的中文名，或者它的代码。

但如果我们使用的数据源（比如QMT）没有提供这个信息呢？这时我们就需要通过第三方库来将汉字转换成为拼音。

这里的难点在于多音字，比如，平安银行应该转换成PAYH，而不是PAYX。我们考察了好几个python第三方库，比如pinyin, xpinyin，最后发现只有pypinyin能较好地实现这个功能。

## 功能介绍

pypinyin库在github上获得了4.6k stars。与之相对照，xpinyin有800多个stars，pinyin是超过200个stars。

你可能会好奇，这个功能主要是什么人在用，为什么能拿到这么多star。这么多star，可能主要是做AI的人给的。

---

将汉字转换成拼音再进行深度学习，是内容审查的一个研究方向。

pypinyin成功的原因主要是在多数情况下，能给出正确的拼音。如果遇到无法正确处理的词，我们还可以通过自定义词组拼音库来进行修正。其次，它提供了简单的繁体支持、多种注意风格支持等。

## 安装和使用

我们通过下面的命令来安装：

```python
pip install pypinyin
```

它主要提供了两个API，即pinyin和lazy_pinyin。但在使用时，我们还需要指定风格(Style)。下面我们看几个简单的例子：

```python
>>> from pypinyin import pinyin, lazy_pinyin, Style
>>> pinyin('中心')
[['zhōng'], ['xīn']]

# 启用多音字模式
>>> pinyin('中心', heteronym=True) 
[['zhōng', 'zhòng'], ['xīn']]

# lazy_pinyin
>>> lazy_pinyin('中国平安') 
['zhong', 'guo', 'ping', 'an']
```

---

lazy_pinyin这个API的特点是（与pinyin相比），它的返回值中，每一个字都只包含一个读音，因此，对每一个字，它返回的是一个字符串，而不是一个数组。

我们来看看它会不会把中国银行拼成zhong guo yin xing:

```python
>>> lazy_pinyin('中国银行') 
['zhong', 'guo', 'yin', 'hang']
```

这个结果是正确的。再回到我们最初的问题，如何得到拼音首字母呢？这就需要我们传入style参数了：

```python
>>> lazy_pinyin('中国银行', style=Style.FIRST_LETTER) 
['z', 'g', 'y', 'h']

# 将其转换成为大写
>>> py = lazy_pinyin('中国银行', style=Style.FIRST_LETTER)
>>> "".join(py).upper()
'ZGYH'

```
这里我们传入的参数是Style.FIRST_LETTER。还有一个与此相混淆的参数，style.INITIALS。如果我们传入此参数：

```python
>>> lazy_pinyin('中国银行', style=Style.INITIALS)
['zh', 'g', '', 'h']
```

结果可能令人意外。要理解它的输出，需要一些拼音的知识。我们只要记住，要得到拼音首字母，应该传入Style.FIRST_LETTER参数。

令人吃惊的是，通过pypinyin给出的首字母结果，竟然比聚宽给出的结果要正确。

---

比如，像重药控股，该公司处在重庆，因此第一个字应该发音chong。聚宽数据给出的拼音是ZYKG，而不是CYKG。又比如长源电力，该公司地处湖北，“长”字可能来源于长江，因此一般读出Chang Yuan Dian Li，聚宽的数据给出的结果是ZYDL。再比如，聚宽拼音一般把晟拼作Cheng，因此象广晟有色会拼成GCYS，而正确的拼法是GSYS。这样的不同之处，大约有30多个。

但pypinyin也有出错的时候，比如重庆港会拼成ZQG。此时，我们就需要使用自定义词典了：

```python
>>> from pypinyin import load_phrases_dict, lazy_pinyin, Style

>>> load_phrases_dict( {"重庆港": [[u"c"], [u"q"], [u"g"]]}, style=Style.FIRST_LETTER)
>>> lazy_pinyin("重庆港", style=Style.FIRST_LETTER)
['c', 'q', 'g']
```

由于我们只关心首字母，因此在加载自定义词典时，指定了Style.FIRST_LETTER，这样将只影响后面对此类风格的查询。

如果你想了解哪些拼音聚宽给出的与pypinyin不一样，可以通过下面的代码来检查：

```python
from pypinyin import Style, lazy_pinyin

for code in await Security.select().eval():
    name = await Security.alias(code)
    jq = await Security.name(code)
    py = "".join(lazy_pinyin(name, style=Style.FIRST_LETTER)).upper()
    if jq != py:
        print(name, py, jq)
```
