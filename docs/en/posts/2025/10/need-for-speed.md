---
title: "China Customs Probe: The End of the Hardware Race in HFT"
date: 2025-10-11
slug: en/posts/uncategory/need-for-speed
tags: [High-Frequency Trading, Hardware Race, Quantitative Investing, Regulatory Compliance]
excerpt: "Three foreign HFT giants face customs probes, exposing the hardware race. As latency gains vanish, firms pivot to hybrid models, blending machine learning with fundamental value discovery."
lang: en
translation_of: posts/uncategory/need-for-speed
auto_translated: true
source_sha: dbba9047f02a8b8663280a3e3c2d6d1a005383c5
cover: "https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/landscape/bakery/11.jpg"
---

Recently, three foreign high-frequency trading (HFT) giants were investigated by China Customs. This event has unveiled an open secret in the HFT world: the **Hardware Race**.

In fact, there are two open secrets in the HFT domain: the hardware race and regulatory arbitrage. These are the only two secrets that allow quantitative giants to earn staggering profits in such an intensely speculative arena. In July this year, we discussed in *"The Elephant in the Room: The Quant Dilemma Under Alpha Decay"* how Jane Street was penalized by regulators in India—a case where a quantitative giant obtained illegitimate profits through regulatory arbitrage.

I have always supported **minimal regulation, letting the market self-regulate**. However, I strongly advocate for regulation in the HFT sector. HFT is not even speculation, because speculation involves a form of risk博弈 (betting); HFT is essentially robbery. Such elephants must be driven out of the room and locked in a cage.

## 01 How the Hardware Race Works

Most HFT strategies are actually quite low-tech (specifically regarding algorithms): in nanosecond-level trading, complex algorithms cannot be executed, and if an algorithm fails, no one can afford to lose money at nanosecond speeds.

Therefore, most strategies essentially profit from bid-ask spreads and time differences; sometimes even artificially creating bid-ask spreads through spoofing. Since algorithms lack complexity, the difficulty shifts to being the first mover. The general approach involves customizing hardware, or even customizing networks.

### Fiber Optics Are Too Slow

Some quantitative giants have already adopted microwave communication instead of fiber optics for data transmission. Why?

There are three main reasons:

First, a widely accepted industry rule of thumb is that the actual laid length of fiber optic cables is typically **1.4 to 1.6 times** the straight-line geographic distance between two points. This means the fiber path is 40%–60% longer than the straight-line path (microwave towers can establish nearly straight line-of-sight propagation).

For example, the route between Chicago and New York is the most critical line in global HFT, connecting the Chicago Mercantile Exchange (CME) in Chicago to data centers at exchanges like Nasdaq in New Jersey.

The straight-line distance between the two cities is approximately 1,150 km. The theoretical fastest time is $1,150 \text{ km} / 300,000 \text{ km/s} \approx 3.83 \text{ ms}$. The latest microwave networks have achieved one-way latency of around 4.0 ms on this route, which is very close to the theoretical physical limit.

Second, the speed of light in glass (fiber optics are made of quartz glass) is approximately 204,000 km/s, significantly lower than the speed of light in a vacuum.

Third, light does not travel along the center of the fiber optic cable; it strikes the interface between the core and the cladding at a specific angle. Since light travels from a medium with a higher refractive index to one with a lower refractive index, and the angle of incidence is large enough (greater than the critical angle), light undergoes **total internal reflection**, bouncing back into the core like a mirror.

Consequently, the actual propagation path of light is a continuous "Z" shape or spiral zigzag, not a straight line. The length of this zigzag is approximately 101.5% of the physical length of the fiber.

These three factors can be collectively termed **path penalty**. In addition, commercial networks suffer from excessive routing hops and uncertain network path lengths. These factors combined allow quantitative giants to receive market data at least 6.7 ms faster than other investors.

In HFT, a difference of milliseconds is not just a few nanoseconds ahead; it is light-years ahead.

### CPUs and Network Cards Are Still Not Fast Enough

Even with the fastest microwave lines, quantitative giants remain unsatisfied when market data packets arrive at servers at near-light speeds (partly due to competitive pressure). At this point, they identify a new bottleneck: **server internal processing latency**.

Traditional data processing follows the path: `NIC -> OS -> CPU -> Trading Program`. For HFT, every step is as slow as a stroll. This process includes NIC reception, hardware interrupts notifying the OS, CPU user-to-kernel mode switching, data copying, and application processing delays. Simply put, no matter how much you optimize, microsecond-level latency remains.

To compete for these microsecond-level delays, using **FPGAs** (Field-Programmable Gate Arrays) provides an easy solution. As semi-custom chips, FPGAs execute programs via hardware circuits and connect directly to NIC chips. When data arrives, it bypasses the CPU entirely, entering the FPGA chip for calculation until a response signal is issued.

FPGAs can reduce latency to the nanosecond level.

### Can You Just Steal It?

Yes, you can. This involves locating data centers next to exchanges. You can take many roads to Rome via microwaves and FPGAs, but some people are simply born in Rome.

However, the hardware race has basically reached its end. As regulation tightens, HFT traders are increasingly inclined to take risks, obtaining illegitimate profits through regulatory arbitrage. We have detailed this part in *"The Elephant in the Room: The Quant Dilemma Under Alpha Decay."*

## 02 Rediscovering Value

Where is the future for quantitative giants?

A recent news item is quite interesting. Prominent quantitative investment firm **Qube** (market cap $34 billion) has formed a team of human stock pickers. Each analyst was allocated an initial capital of $200–500 million for trading and research.

Qube is not the first pure-quant firm to shift to a hybrid model; previously, giants like D.E. Shaw, Engineers Gate, and Squarepoint have already moved to hybrid models. Clearly, human traders’ strategies will not be HFT strategies; they will return more to the essence of investing—discovering value itself.

This may be the path every quantitative giant must take.
