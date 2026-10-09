---
title: "How to Search Stock Codes by Pinyin Initials in Python"
date: 2024-03-24
slug: en/posts/python/pypinyin
tags: [Python, Pinyin Search, Market Data]
excerpt: "Type ZGPA to instantly find Ping An Insurance (中国平安) — a standard terminal trick. This guide shows how to build pinyin-initial search for China A-shares in Python with pypinyin."
lang: en
translation_of: posts/python/pypinyin
auto_translated: true
source_sha: e3dd4d718080bb248de8873bbe346c4b75bb6a22
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/03/pypinyin.png"
---

Searching securities by pinyin initials is a niche feature only a handful of quants will ever need — but once you've used it, you can't live without it. Type `ZGPA` and you instantly get Ping An Insurance (中国平安) or its ticker. It's standard in every market-data terminal.

Under the hood, it's all about converting Chinese characters to pinyin. Some data vendors already ship this mapping, but many don't.

---

If your data source is JQData (jqdatasdk), `jq.get_all_securities` returns a security master table with:

* index, security code, e.g. 000001.XSHE
* display_name, Chinese name, e.g. Ping An Bank (平安银行)
* name, pinyin-initial name, e.g. PAYH
* start_date, IPO date
* end_date, delisting date. Only populated for delisted securities.
* type, security type, e.g. stock, index, fund.

The lookup we need lives in the `name` field, mapped against `index` and `display_name`. When a user types PAYH, you just search this table to return the Chinese name or the ticker.

But what if your data source — QMT, for example — doesn't provide this field? Then you need a third-party library to convert Chinese to pinyin.

The hard part is polyphonic characters. Ping An Bank (平安银行) should map to PAYH, not PAYX. We tested several Python libraries, including pinyin and xpinyin, and only pypinyin handled this reliably.

## Overview

pypinyin has 4.6k stars on GitHub. By comparison, xpinyin has 800+ stars, and pinyin has 200+ stars.

You might wonder who actually uses a Chinese-to-pinyin library, and why it earned that many stars. The answer is most likely AI developers.

---

Converting Chinese characters to pinyin before deep learning is a known research direction in content moderation.

pypinyin stands out because it gets the pronunciation right in most cases. When it doesn't, you can fix it with a custom phrase dictionary. It also offers basic Traditional Chinese support, multiple pinyin styles, and more.

## Installation and Usage

Install it with:

```python
pip install pypinyin
```

It exposes two main APIs, `pinyin` and `lazy_pinyin`, plus a `Style` option to control the output format. Here are a few quick examples:

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

Compared with `pinyin`, the `lazy_pinyin` API returns only one pronunciation per character, so each character maps to a string rather than a list.

Let's check whether it correctly renders Bank of China (中国银行) as zhong guo yin hang:

```python
>>> lazy_pinyin('中国银行') 
['zhong', 'guo', 'yin', 'hang']
```

That result is correct. Back to our original question — how do we get just the initials? Pass in the `style` parameter:

```python
>>> lazy_pinyin('中国银行', style=Style.FIRST_LETTER) 
['z', 'g', 'y', 'h']

# 将其转换成为大写
>>> py = lazy_pinyin('中国银行', style=Style.FIRST_LETTER)
>>> "".join(py).upper()
'ZGYH'

```
Here we pass `Style.FIRST_LETTER`. Don't confuse it with another similar option, `Style.INITIALS`. If we pass that instead:

```python
>>> lazy_pinyin('中国银行', style=Style.INITIALS)
['zh', 'g', '', 'h']
```

The output can be surprising unless you know some pinyin linguistics. Just remember: to get pinyin initials, always use `Style.FIRST_LETTER`.

Surprisingly, pypinyin's initials turn out to be even more accurate than JQData's.

---

Take Chongqing Pharmaceutical Holding (重药控股), a Chongqing-based company, so the first character 重 should read “chong”. JQData gives ZYKG instead of CYKG. Another example is Changyuan Power (长源电力), based in Hubei, where 长 likely comes from the Yangtze River (长江), so it should read Chang Yuan Dian Li — but JQData gives ZYDL. JQData also tends to render 晟 as “cheng”, so Guangsheng Nonferrous (广晟有色) becomes GCYS instead of the correct GSYS. There are about 30 such mismatches in total.

But pypinyin makes mistakes too — Chongqing Port (重庆港) comes out as ZQG. That's when you need a custom dictionary:

```python
>>> from pypinyin import load_phrases_dict, lazy_pinyin, Style

>>> load_phrases_dict( {"重庆港": [[u"c"], [u"q"], [u"g"]]}, style=Style.FIRST_LETTER)
>>> lazy_pinyin("重庆港", style=Style.FIRST_LETTER)
['c', 'q', 'g']
```

Since we only care about initials here, we load the custom dictionary with `Style.FIRST_LETTER`, so it only affects queries in that style.

If you want to find all the cases where JQData differs from pypinyin, you can check with:

```python
from pypinyin import Style, lazy_pinyin

for code in await Security.select().eval():
    name = await Security.alias(code)
    jq = await Security.name(code)
    py = "".join(lazy_pinyin(name, style=Style.FIRST_LETTER)).upper()
    if jq != py:
        print(name, py, jq)
```
