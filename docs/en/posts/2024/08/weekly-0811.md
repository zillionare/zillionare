---
title: "Citadel Quant Internship: Datathon Strategy & Market Recap"
date: 2024-08-11
slug: en/posts/uncategory/weekly-0811
tags: [Quantitative Trading, Citadel Datathon, Market Analysis, Time Series]
excerpt: "Master Citadel’s Datathon for quant roles. Analyze July CPI/PPI, Fed data, and US equity trends. Explore tsfresh for time-series feature extraction in quantitative trading."
lang: en
translation_of: posts/uncategory/weekly-0811
auto_translated: true
source_sha: bc5bb271ebf1038f2b592a860c75aa9b015c17b1
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/kenneth-griffin.jpg"
---

## This Week's Highlights

*   The central bank announced increased treasury bond trading in open market operations, firmly preventing exchange rate overshoot risks.
*   National Bureau of Statistics: July CPI rose 0.5% year-over-year (YoY), while PPI fell 0.8% YoY.
*   US initial jobless claims dropped significantly, easing recession fears and driving volatile but positive US equity recovery.

## Next Week's Watchlist

*   US PPI (Tuesday night), core CPI (Wednesday night), and retail sales data (Thursday).
*   Friday (August 16) is the stock index futures expiration date.
*   Monday: Elon Musk connects with Donald Trump.

## This Week's Selection

*   Datathon: My Path to a Citadel Quant Role! Includes past competition materials.
*   Even video calls can't be trusted! Deep-Live-Cam went viral overnight; fake live streams require only one photo.
*   Introducing a Quant Library: tsfresh

---

<remark>In the previous edition's <b>Highlights</b>, we mentioned the BASF explosion and soaring vitamin prices. This week, the vitamin sector rose 3.6%, with a peak increase of 6.7%.</remark>

*   Over the weekend, the central bank issued multiple statements to improve the financial support system for housing rentals and support destocking of existing commercial housing. It also studied narrowing the interest rate corridor width. Measures include monitoring cross-border capital flows to prevent one-sided consistent expectations from self-reinforcing and firmly preventing exchange rate overshoot risks. <remark>The interest rate corridor refers to the range of short-term money market interest rates set by the central bank. It typically consists of three rates: <br>Policy Rate: Usually the central bank's benchmark rate, such as the rediscount rate or reserve requirement rate.<br>Excess Reserve Rate (Upper Bound): Interest earned on excess reserves held by banks at the central bank.<br>Overnight Interbank Rate (Lower Bound): The minimum borrowing cost in the interbank market.</remark>
*   July CPI rose 0.5% YoY, up from 0.3% previously. Pork prices surged 20.4%, contributing 0.24% to the CPI increase. Livestock and meat prices rose 4.9%, contributing approximately 0.14% to the CPI. Affected by weak market demand and falling prices of some international commodities, PPI fell 0.8%, down 0.2% month-over-month (MoM). <br><remark>Pork alone drove nearly half of the CPI increase. The rapid short-term rise in pork prices is unlikely to sustain, posing pressure on next month's CPI MoM.</remark>
*   Global stock markets experienced significant volatility previously due to rising July unemployment, Warren Buffett's substantial position reduction, and the Bank of Japan's rate hike. US stocks endured the most volatile week of 2024. However, on August 8, the US reported initial jobless claims of 233,000 for the previous week, down from 250,000 previously and below the expected 240,000. Following this data, which significantly exceeded expectations, market concerns eased. US stocks and the Nikkei index fell initially but then rose, basically recovering lost ground. This event indicates that the market is currently extremely sensitive to data reports.

---

*   On Friday, it was reported that Zhao Xuejun, Chairman of Harvest Fund Management, is cooperating with relevant departments for investigation due to personal issues. Liu Zhangming, Director of Founder Securities Research Institute, was adjusted to Deputy Director and will no longer serve as the administrative head of the institute. Liu was issued a warning letter in January for违规荐股 (违规荐股/irregular stock recommendations).

## Next Week's Watchlist

*   Next Tuesday, Wednesday, and Thursday will see several key data releases regarding Fed rate cuts, including PPI, CPI, and retail sales. Hawkish Fed officials stated that inflation remains well above the committee's 2% target and carries upside risks. Regarding earnings, Home Depot and Walmart are worth watching; hypermarkets at the end of the commodity supply chain may have a more tangible sense of whether inflation is accelerating or decelerating.
*   Friday (August 16) is the stock index futures expiration date. This year, the Shanghai Composite Index has shown relatively stable performance, even trending upward, on index futures expiration dates.

<claimer>Compiled from sources including Cailian Press, Eastmoney, and Securities Times.</claimer>

---

# DATATHON: My Path to a Citadel Quant Role! Includes Past Competition Materials

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261005065601-Citadel_Intenship_KenSpeakstoInterns_YT_v2.jpg)
<cap>Kenneth Griffin Speaks to Interns</cap>

Citadel is a top-tier global hedge fund management company, founded by Kenneth Griffin in 1990, and is the dream company for many quants.

Citadel offers various roles for fresh graduates, but often requires an internship first.

Gaining internship eligibility at Citadel is challenging. This article introduces some tips for passing the process.

---

We will introduce the three main categories of roles: **Investment**, **Quantitative Research**, and **Software Development**, with a focus on Quantitative Research positions.

We will outline a shortcut to obtaining a Quantitative Research role and provide important preparation materials.

<!--
## Wonderlic Test

The Citadel online assessment test, also known as the Citadel Wonderlic Test, is essentially a psychometric assessment designed to measure various skills that cannot be evaluated by reviewing a candidate's resume or observing their work performance. - Interviews. These skills include decision-making, problem-solving, the ability to learn new information, and adapting to a changing work environment.

Citadel also uses this test to streamline the hiring process. As a company with this capability, it receives thousands of applications for all positions annually. Therefore, using a tool like Wonderlic to eliminate unqualified candidates from the start, rather than spending significant time and resources on face-to-face interviews, makes sense.

50 questions, 12 minutes, 14 seconds per question. Prep courses can be found online, typically costing between $500 and $1,000.

Wonderlic Select is not the only Citadel assessment. If you are applying for a Citadel Software Engineer internship, you may face a HackerRank coding assessment. If you apply for a Citadel Trading Internship, you will be required to take the Citadel Financial Concepts Assessment Test (Citadel FCAT).

-->

---

## Investment Roles

Investment roles are likely the most difficult to apply for but offer excellent compensation.

2025 undergraduate or master's interns will receive a weekly salary of $5,300, with the first week spent staying at a Four Seasons hotel to facilitate rapid adaptation and socialization among peers.

Regarding application requirements, current major and school background are not critical; you do not even need to be an economics or finance major, but you must be interested in stock valuation.

However, their requirement is "Extraordinary" -- this standard of extraordinariness is actually higher than Harvard's admission standards. Citadel claims a 1% acceptance rate, compared to Harvard's 4%. To give an example of "extraordinary," Citadel mentions hiring NASA astronauts.

Therefore, it is difficult to give specific advice for this role. However, Citadel collaborates with Wonderlic for interview screening. If you are determined to apply for this role, we recommend taking a Wonderlic training course, costing approximately $50. Wonderlic Select includes cognitive, psychological, cultural, and logical tests. Taking such training will help you filter out unprepared candidates.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/11-weeks-of-extraordianry-growth.jpg)
<cap>11 weeks of extraordinary growth program</cap>

---

Once selected as an intern, Citadel provides an 11-week on-the-job training program. This training helps you grow rapidly, and the probability of being retained after the program is high.

## Software Development Roles

This role is easier to apply for. After Citadel conducts a basic screening, it will quickly invite you to take the HackerRank test. Since HackerRank is automated, almost everyone who applies receives an invitation.

You may encounter Hard-level questions from LeetCode on HackerRank, but some have reported unexpectedly encountering Easy-level questions. Overall, practicing LeetCode regularly is helpful. The more fully prepared you are, the greater your chances of success.

You can find leaked Citadel interview questions on Glassdoor or 1point3acres, although most information requires payment.

## Quantitative Research and Datathon

Participating in Datathon and achieving good rankings is the shortcut to obtaining an internship in a **Quantitative Research Role**. Based on historical competition data, the number of competitors is not very large (analyzed from valid submission IDs), and there are two opportunities per year.

This competition is hosted by Correlation One. C1 was founded by former hedge fund manager Rasheed Sabar, focusing on helping enterprises and developing talent through training solutions.

Its partners include well-known companies such as DoD, Amazon, Citadel, and Point72. Due to the founder's previous professional network, it secured the opportunity to host competitions and recruit for Citadel and Point72. You can also check their website for some training and recruitment programs.

---

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/correlation-one.jpg)
<cap>Correlation One</cap>

Datathon is only for current students; you must use a school email to apply. After online registration via the official website, you must first take a **90-minute** online assessment. This assessment includes psychological and value-based questions, as well as some technical questions.

Assessment results will be notified **three days before the competition**. Then, you enter a networking session, where you need to form a team or join an existing one. Datathon is a collaborative project, generally requiring teams of **4 people**.

After the official start, you will receive problems and datasets from the organizers (**we have collected past test questions, datasets, and submitted answers from participating teams on our website; see the end of the article for the address**). You need to select one problem to research and submit a report within 7 days, outlining your research.

This process may be unfamiliar to students in mainland China, but for overseas students, similar collaboration and team presentations are common tasks. Therefore, mainland students who wish to participate need more practice in this area; otherwise, they may feel that 7 days is too rushed.

---

## Benefits for Women

In addition to the regular Datathon, women can participate in the exclusive Women's Datathon. The most recent one is scheduled for January 10 next year; now is the perfect time to start preparing.

However, this Women's Datathon is offline and limited to students currently studying in the US and Canada.

## Datathon Passing Tips

Datathon appears to test data analysis skills, which are hard skills. In reality, familiarizing yourself with the rules and ensuring effective team collaboration are also very important. Moreover, from a corporate culture perspective, Citadel places great emphasis on collaboration.

1.  When forming a team, ensure that team members use the same programming language; otherwise, work results cannot be aggregated.
2.  Although Citadel does not restrict programming languages or software tools, the final report must be in PDF, PPT, or HTML format. Additionally, if your submitted PDF contains formulas, you must also provide the LaTeX source code. Considering the competition lasts only 7 days, you must be very familiar with these tools beforehand. Alternatively, when forming a team, consider ensuring that at least one team member possesses similar skills.
3.  Datathon is an online virtual competition, so there is no on-site presentation environment. Therefore, you must be fully familiar with and adhere to its submission specifications.
4.  Precisely because of the previous point, the Report must be well-organized. Read it multiple times from an outsider's perspective to see if someone outside the project can gain a clear impression from reading it.
5.  Familiarize yourself with Jupyter Notebook and pandas (if you use Python). This is also officially recommended; Notebooks allow you to quickly browse the datasets provided by the competition.

---

6.  Supplementary data is beneficial as it reflects your ability to solve problems outside the box. Therefore, familiarize yourself with various datasets regularly. If you need to scrape data on the fly, you must be very familiar with web scraping. Since scraping is serial to subsequent data analysis, other work must wait until data is obtained.
7.  Visualization is crucial. If you are accustomed to using Python, practice the matplotlib and seaborn libraries regularly.

We have collected all competition questions since 2017, including data, questions, and reports and code submitted by some teams. If you need to prepare for Datathon, this will be an excellent reference.

Here, we provide a brief introduction to the Summer 2024 Datathon.

## 2024 Summer Datathon

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/datathon-2024-summer-ps.jpg)
<cap>Problem Statement of 2024 Summer Datathon</cap>

The 2024 Datathon concluded on August 5. This year's topic concerned junk food, requiring conclusions about US food processing from the provided dataset. In addition to the specified dataset, you were allowed to add new datasets as needed. However, these datasets were also submitted to the judges and must not exceed 2GB.

Topics could be chosen from the following three or self-proposed:

---

1.  Can restaurant stock prices be predicted from meat production?
2.  Does sugar price affect young people's consumption of sugary drinks? If there is an impact, does it vary by region?
3.  Is there a correlation between troughs in meat production and unemployment numbers?

Some teams have uploaded competition datasets, questions, and their answers to GitHub. The table below lists some repos we have collected. It includes solutions from teams that ranked in previous years, which are highly worth studying. If you can reach this standard in your practice, you have a high probability of ranking in your own competition.

| year                                                                         | rank | files              | Description                  |
| ---------------------------------------------------------------------------- | ---- | ------------------ | ---------------------------- |
| [2024 summer](https://github.com/arjashok/2024-Summer-Datathon)              | NA   | data, code, report | Reports from two teams, runnable |
| [2024 spring](https://github.com/chtang-hmc/Spring-Invitation-Datathon-2024) | NA   | data, code, report | Clear directory, high-quality report |
| [2023](https://github.com/redders7/datathon2023)                             | NA   | report, code       |                              |
| [2022](https://github.com/Bennyoooo/citadel_datathon_2022)                   | 3rd  | report, code       | High-quality report, good visualization |
| [2021 summer](https://github.com/joshuali99/Citadel-Summer-Datathon-2021)    | 1st  | data, src, report  | Includes Airbnb data         |
| [2021 spring](https://github.com/evilpegasus/datathon-spring-2021)           | NA   | data,code,report   |                              |
| [2020]                                                                       | 3rd  | report             |                              |
| [2018](https://github.com/wlong0827/citadel-datathon-2018)                   | 1st  | data,code,report   | Reports from two teams       |
| [2017]                                                                       | NA   | report,code,data   |                              |

These competition materials have also been uploaded to our Jupyter Lab server. For a small fee, you can use them. Without downloading or installing anything, you can run and debug answers submitted by others.

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/datathon-screenshot.jpg)
<cap>Datathon Historical Materials</cap>

---

If you want to start practicing immediately, you can [apply to use our course environment](https://mp.weixin.qq.com/s?__biz=MzI2MzE3MzY4Ng==&mid=2662263140&idx=1&sn=e0e0f226e385d2f3866a016b5886c2c7&chksm=f1e5aa3dc692232bcad109555676aed1cd86e6af4ca117f1cb9b195ae82a6addeb2e1b1bb9f7&payreadticket=HGygwRghkKW2urwKdqW4GaeGTsLWib7U82M8r7Pj7Sw9-POZVrrNC5iMskYZQYG_UM2u5BM#rd). This saves you time downloading data and installing environments. We have already debugged the code for the Summer 2024 competition, allowing you to learn from others' code while running it.

---

# Video Calls Can No Longer Be Trusted! DEEP-LIVE-CAM Went Viral Overnight; Fake Live Streams Require Only One Photo!

![L50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/deep-live-cam.png)

Get Elon Musk to promote your products!

AI face-swapping is no longer a major news item, and video face-swapping has long been realized, with Deep Fake being the earliest example. But what if live streams and video calls could also be face-swapped in real-time?

Deep Live Cam, released several months ago, went viral overnight. Many people noticed that it can fake live streams using only one photo.

Recently, blogger Matthew Berman conducted a test. He was live-streaming in front of the camera wearing glasses. When he provided the model with a photo
