---
title: "Remembering Daniel Kahneman, Founder of Behavioral Economics"
date: 2024-04-01
slug: en/posts/career-figure/Daniel-Kahneman
tags: [Behavioral Economics, Prospect Theory, Quantitative Investing]
excerpt: "Daniel Kahneman, founder of behavioral economics, died on March 27. His Prospect Theory formalized psychology in economics and underpins behavioral finance in quantitative investing."
lang: en
translation_of: posts/career-figure/Daniel-Kahneman
auto_translated: true
source_sha: 5759e41b40bf6cd8b56aa42af11ddaed12a35867
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/04/Hebrew.jpg"
---

On March 27, Daniel Kahneman, the founding father of behavioral economics, passed away. As a branch of behavioral economics, behavioral finance is now widely used in quant, successfully explaining many drivers of price fluctuations along the time-series dimension.

Kahneman's key contribution was to create a formal framework that brought the use of psychology to explain and predict economic behavior into the realm of science.

---

A while ago, I was chatting with a student who told me, **markets can give birth to everything, except the market itself**. The line is profound, surprisingly concise, and rhetorically beautiful.

Not every economist grasps this truth, yet I heard such profound insight from a student. I feel honored and inspired: beyond sharing pure quant knowledge, I should also share some of my own reflections from studying economics — they may benefit some readers, just as I benefited from that conversation.

As that student put it:

!!! quote
    What we can do is share these economic ideas with friends around us, letting them spread and propagate, so that after a few generations, things will slowly start to change.

Yes, this matters. If more people pay attention to, learn, and study economics, more people will rediscover logic and common sense through economics — and the future will be much brighter.

Be the change you seek!

## Kahneman and Behavioral Economics

Kahneman was Jewish, born in Tel Aviv. During World War II in Paris, his family was rounded up by the Nazis, but his father's employer managed to rescue them — another Schindler's List-type story.

---

<div class="L50">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/03/Daniel_Kahneman_(3283955327)_(cropped).jpg">
<cap>Image from wiki, used under CC BY 2.0</cap>
</div>

After the war, he studied psychology at the Hebrew University and earned his PhD in psychology from UC Berkeley. Although he won the Nobel Prize in Economics, he never received formal training in economics.

In March 1979, Kahneman and his collaborator Amos Tversky published the paper *Prospect Theory: An Analysis of Decision under Risk*, introducing prospect theory. Since publication, the paper has garnered over 80,000 citations.

Since Adam Smith, mainstream economics had assumed that every human decision is "economically rational," but reality says otherwise. Prospect theory introduced asymmetric psychological utility around gains and losses and high versus low probabilities, successfully explaining many seemingly irrational phenomena.

!!! tip
    Kahneman's close friend Amos Tversky died of melanoma in 1996, missing out on the Nobel Prize. Kahneman and Tversky shared a decades-long friendship and co-authored several foundational works in behavioral economics. Tversky's wife once said their bond was deeper than anyone else's, even deeper than marriage. In fact, the two were opposites in daily habits (early riser vs. night owl) and personality (introvert vs. extrovert). They were inseparable, like John Lennon and Paul McCartney of the Beatles.

--- 

Beyond his academic achievements, Kahneman was also the author of the bestseller **Thinking, Fast and Slow**.

Prospect theory holds that choices under uncertainty depend on the gap between outcomes and expectations (the reference point), not on outcomes alone.

Suppose two advisors pitch the same fund to the same investor. The first emphasizes only that the fund averaged a 10% return over the past three years; the second adds that while the fund beat the market average over the past decade, it has been declining for the last three years.

Prospect theory predicts the investor is far more likely to buy from the first advisor, even though the fund is identical. Because people exhibit loss aversion, when offered one option framed as a potential gain and another framed as a potential loss, they will choose the former.

Prospect theory describes the decision process as a function, proposing the following prospect value function:

$$
U = \sum_{i=1}^{n} \pi(p_i)v(x_i)
$$

Here, $x_i$ are the possible outcomes (although they are random variables, they follow a probability distribution and can be considered objective), and $p_i$ are the probabilities of those outcomes.

The probability weighting function $\pi(p)$ and the value function $v(x)$ are the two core functions of prospect theory, both nonlinear.
---

Let's start with the value function $v(x)$.

The value function $v$ is an asymmetric $S$-shaped function: concave above the psychological neutral reference point — in the gain domain — and convex below it — in the loss domain. As a result, each additional unit of gain (or loss) yields diminishing **value**. In other words, the subjective feeling of moving from 0 to 100 in gains is stronger than moving from 100 to 200. Moreover, the value function is steeper in the loss domain, meaning **the pain of losing 100 yuan exceeds the pleasure of gaining 100 yuan**.

<div class="L50">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/04/value-function.jpg">
<cap>Image source: sciencedirect.com</cap>
</div>

Note that in the value function, prospect theory begins to distinguish objective value from subjective value — see the two axes in the chart above. We'll discuss why this matters at the end of this article.

The probability weighting function $\pi$ describes the relationship between an event's objective probability and its subjective perception. Simply put, low-probability events (such as death in freak accidents) tend to be overweighted, while high-probability events (such as death from heart disease or cancer) are underweighted. It is likewise modeled as a nonlinear (sigmoid-type) function, though its exact shape must be estimated empirically for each specific gamble.

The following example illustrates prospect theory in action. Suppose the insured risk has a 1% probability, a potential loss of $1,000, and a premium of $15. If we set the reference point at current wealth, then:

---

1. Paying $15 for insurance yields a prospect utility of $v(-15)$, note this is not -15, but a function of it.
2. Not buying insurance means a $1,000 loss with 1% probability if the accident occurs, or $0 loss with 99% probability. The prospect utility in this case is:

$$
\pi(0.01) \times v(-1000) + \pi(0.99) \times v(0) = \\
\pi(0.01) \times v(-1000)
$$

Here comes the crucial part. According to prospect theory:
1. $\pi(0.01) > 0.01$, because small probabilities are overweighted.
2. $v(-15)/v(-1000) > 0.015$, which follows from the convexity of the value function in the loss domain (if it were linear, both sides would be equal).

From 1) and 2) above, it follows that:

$$
\pi(0.01) \times v(-1000) < v(-15)
$$

In other words, because we overweight small-probability events, when evaluating an event that objectively occurs with only 1% probability, we treat it as if it were more than 1%. The resulting expected loss looms larger than -$15, which is why we tend to buy the insurance.

## The Underrated Field of Behavioral Economics

Kahneman's passing seems to have drawn little attention in the Chinese-speaking world. The few tributes I saw remembered him mostly as the author of *Thinking, Fast and Slow*.

---

<div class="L33">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/04/think-fast-and-slow.jpg">
<cap>Thinking, Fast and Slow. Image from Douban</cap>
</div>

Kahneman's importance lies in his pioneering work. He not only brought psychology into economic research, but more importantly provided a formal method for doing so. I believe many before him had explored psychological explanations for economic activity, but without formal methods and mathematical models, such work could not enter the scientific mainstream.

Kahneman and Tversky succeeded by using the language of mathematics to lay a foundational framework for behavioral economics, enabling later scholars like Thaler to carry the field forward.


Another key contribution: since Adam Smith, the rational agent has been a central assumption in economics. Everyone knew this assumption was limited, but there was no effective example of how economics could move forward without it. In its own narrow domain, behavioral economics successfully discarded the rational-agent assumption, introduced the concept of subjective value, and made subjective value calculable.

One of the most fundamental questions in economics is the distinction between subjective and objective value.

Some theories hold that value is congealed, undifferentiated human labor embodied in commodities, and therefore objective. The longer and more complex the production process, the higher the value — entirely independent of subsequent exchange (an unsold good has the same value as a sold one, as long as production time is identical).

---

This can indeed explain many economic phenomena, but not this one: producing 10,000 tons of cement creates the value of 10,000 tons of cement; yet producing 100 million tons (global output in 2021 was 4.4 billion tons) creates no value at all — instead it causes ecological disaster. Needless to say, it cannot explain economic behavior around beauty, tourism, or art.

The subjective theory of value, by contrast, holds that the value of a good is determined not by its intrinsic objective properties or the socially necessary labor to produce it, but by how much the acting individual believes it helps achieve their desired ends.

In essence, **the subjective theory of value is human-centered: what you need is what has value**.

Subjective value theory can explain a broader range of economic phenomena. For example, the same pile of dung is a delicacy of great value to a dung beetle, while for a cow, this "valuable" thing required no production, no socially necessary labor time at all — it is mere excrement. This is one phenomenon objective value theory cannot explain.

In this sense, if economics is ever to build a grand unified theory like physics, starting from the postulates of subjective value theory is more likely to get us there.

Although behavioral economics introduces subjective value only in a small slice of economic activity (value exchange) while retaining the notion of objective value, this may be humanity's first attempt to calculate subjective value through formal methods. The significance speaks for itself. This is likely where behavioral economics is truly underrated.
