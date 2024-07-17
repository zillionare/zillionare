---
title: Jane Street出谜，答对入职！
slug: jane-street-puzzles
subtitle: 我与简街，只隔一道谜？！
date: 2024-06-08
img: https://images.jieyu.ai/images/2024/06/john-fawcett.jpg
category:
  - 职场
tags:
  - 职场
  - 资源
  - 公司
---

---
layout: prelude
clicks: 17
---

<style>
.janestreet {
    position: absolute;
    width: 100%;
    animation: jane-motion 50s linear forwards;
}

@keyframes jane-motion {
    0% {
        opacity: 0;
    }

    50% {
        opacity: 1
    }

    100% {
        opacity: 0;
    }
}


</style>


<ColorText v-motion 
           :click-1="{scale:0}"
           :enter="{y:0, scale:1}">Jane Street</ColorText>

<ColorText v-motion
            :click-1="{scale:1,x:75}"
            :click-2="{scale:0}"
            :enter="{scale:0}"
            :duration="1000">
    solving the puzzle of global markets
</ColorText>

<div v-if="$clicks === 2" class="janestreet" v-motion>
<video src="http://localhost:8000/janestreet.mp4" autoplay loop></video>
</div>

<div v-motion
     :click-3="{scale:1, x:300}"
     :click-5="{x: 100}"
     :enter="{scale:0}"
     :duration="1000"
     style="width:300px;position:absolute">
     <img src="http://localhost:8000/puzzle.jpg"/>
</div>

<div v-motion
     :click-4="{scale:1, x:400, y:100}"
     :click-5="{scale:0}"
     :enter="{scale:0}"
     :duration="1000"
     style="width:100px;position:absolute">
     <img src="http://localhost:8000/question.gif"/>
</div>

<div v-motion
    :click-5="{scale:1, x:700, y:100}"
    :enter="{scale:0}"
    :duration="1000"
    style="width:100px;position:absolute">
    <img src="http://localhost:8000/ChessSet.jpg"/>
</div>

<div v-motion
     :click-6="{scale:1, x:600, y:100}"
     :enter="{scale:0}"
     :duration="1000"
     style="width:100px;position:absolute">
     <img src="http://localhost:8000/example.jpg"/>
</div>

<div v-motion style="width:100px;position:absolute;color:red"
    :click-7="{x:640,y:140}"
    :click-8="{x:670,y:140}"
    :click-9="{x:670,y:170}"
    :click-10="{x:640,y:140}"
    :click-11="{x:670,y:140}"
    :click-12="{x:670,y:110}"
    :click-13="{x:640,y:140}"
    :click-14="{x:640,y:170}"
    :click-15="{opacity:0}"
    >★
</div>

<ColorText v-motion
            :click-15="{scale:0.5,x:275,y:-50}"
            :enter="{scale:0}"
            :duration="1000">
    Illinois, Ohio, Utah(Atah), Iowa(Ioha), Idaho(Ieaho)
</ColorText>

<div v-if="$clicks === 16" style="color:red;height:60%;width:100%;background:rgba(0,0,0,0.8);position:absolute;padding: 150px;text-align:center">

## 一半的分数1.65亿是怎么算出来的？

</div>
    
<Promotion/>

<Audio name="wechat-huwo" :delay=500 />

<!--
prelude

简街(JaneStreet)是华尔街最神秘的高频量化交易公司之一。2024年，一季度收入就达到了44亿美元，同比暴涨一倍，净利超60%。



在Jane Street的官网首页，有这样一句logo, **solving the puzzle of global markets**。



量化就像破译密码，就是要解决各种谜题，数字的、逻辑的、甚至没有明确规则的谜题。

正是基于这样的想法，简街干脆在招聘上整起了活儿，开了一个专栏，每个月出一道迷题。
如果你能解决这个谜题，就可以把方案提交给他们，登上排行榜。虽然不能直接拿到offer，但如果你简历投递无门，这倒是个机会。




最新6月的题已出。这道题是这样的



是不是一脸问号？它的目标是在这个5*5的网格中，放置美国州名，并且能通过国王走位拼出州名。



国王走位是国际象棋中，王的移动规则。在国际象棋中，国王可以在以它为中心的九宫格中，移动到任意一个相邻的位置。



比如，在这个3*3格的网格中，我们从中间的I出发，按国王走位的规则，就能拼出伊利诺伊州 -- Inlinois。










在第2步，移动到的字符是N，而实际上伊利诺伊第二个字母是L。但规则允许每个州可以替换一个字母，位置不限，因此只要正确拼出了它的6个字母，剩下一个错了也算对。

每拼出一个州，就按该州人数计分一次。



最终，这个3*3的格子，可以拼出Illinois, Ohio, Utah(Atah), Iowa(Ioha),和Idaho(Ieaho)，这几个州的人数加起来，就是答案的得分，大约3200万分左右。

规则不变，格子数增加到5*5，就是这道题的要求。它还有一个要求，就是至少要得到可用分数的一半以上，即1.65亿分以上。



你知道这个分数是怎么来的吗？如果你知道，可以请你把答案留在评论区吗？



简街除了在美国之外，还在坡县和香港设有办公室。这两地的人如果刷到此视频，也可以留言秀下。到昨天为止，只有不到200人提交了正确答案。如果你对简街感兴趣，快来刷题吧！
-->
