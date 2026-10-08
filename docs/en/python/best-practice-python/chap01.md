---
title: "Why Python? The Case for Quantitative Finance"
date: 
slug: en/articles/python/best-practice-python/chap01
tags: [Python, Quantitative Finance, Software Engineering, Factor Investing]
excerpt: "Python dominates quantitative finance due to its readability, vast ecosystem, and AI integration. This article explores its history, design philosophy, and addresses common misconceptions about performance and scalability in large-scale applications."
lang: en
translation_of: articles/python/best-practice-python/chap01
auto_translated: true
source_sha: 14402688cc86d3f762d61bb90bddec09d47c9d79
---

In 2020, the European Space Agency (ESA) planned to launch a Mars rover to collect rock samples for analysis, aiming to detect signs of life on the planet. Due to fuel constraints, the rover could only return 500g of Martian rocks. Consequently, only carefully selected samples could be brought back. To achieve this, scientists developed an on-site selection system requiring visual reconstruction capabilities, for which they built an artificial neural network. Whether constructing neural networks, managing multi-CPU clusters, or leveraging NVIDIA’s CUDA libraries via PyCUDA, this task relied heavily on Python.

![50%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/202106/mars-67522_1920.jpg)

<cap>Image Source: [mars-rover-space-traveler]</cap>

The first programming language deployed on Mars was Java. It landed on January 4, 2004, as part of the Spirit rover’s system. For this mission, tasked with more complex and intelligent operations, scientists chose Python.

This choice was not surprising. Indeed, with the rise of artificial intelligence, Python has become the most sought-after development language, climbing year after year in the TIOBE Programming Language Index:

![50%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/toibe_2023_rank.png)

Moreover, since TIOBE began compiling its rankings, Python has been named "Language of the Year" five times: in 2021, 2020, 2018, 2010, and 2007. It remains the only language to achieve this distinction five times:

![50%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/toibe_lang_trending.png)

Furthermore, Python’s popularity is evident in the download statistics for its VS Code extension (over 110 million downloads, compared to 60 million for C/C++) and the over 1 billion downloads of Python images on Docker Hub.

So, what kind of language is Python? What are its specific advantages in development that have earned it such a reputation? We often hear (especially in Chinese communities) that Python is unsuitable for large-scale applications. Is this true? This book attempts to answer these questions, particularly from a software engineering perspective, outlining the development processes and standards to follow, as well as the tools and techniques required to rapidly develop complex, large-scale applications.

Python is a development language with a long history, created by Dutch programmer Guido Van Rossum, affectionately known in the Chinese community as "Uncle Gui" (Guido). For 30 years from its inception, Guido guided the language’s future direction with his passion and dedication, earning the title "Benevolent Dictator for Life." He took a brief hiatus around 2018 but returned in 2020 to join Microsoft and continue leading Python’s development.

The initial version of Python was released in January 1994, predating Java[^Java]. Initially, it absorbed many features from Lisp, such as functional programming tools, traces of which remain today in widely used functions like `reduce`, `filter`, and `map`. At that time, Perl was a very popular scripting language, and Python also absorbed many mature modules from it, successfully retaining users who were looking for a replacement for Perl.

Python 2.0 was released in the year 2000. Its most significant change was not in new features, but in process and standards: first, Python developers migrated to a new code management tool, replacing CVS, which had severely hindered team development efficiency due to its lack of support for collaborative development; second, they modeled a PEP (Python Enhancement Proposal) system after RFCs. Any new features or changes had to be proposed, reviewed, and confirmed via PEP before being formally included in the development plan. These changes set Python on the path to success.

The major functional change in this version was the adoption of 16-bit Unicode strings (note: this is not the UTF-8 encoding commonly used today), enabling Python to move beyond the English-speaking cultural sphere and begin its internationalization journey.

In late 2001, Python 2.2 was released, making Python a purely object-oriented programming language. During this period, Java flourished in enterprise applications, while Python found its niche in data and infrastructure management.

In 2008, Python 3.0 was released. Due to its incompatibility with the 2.x series (with Python 2.7 becoming the final version of Python 2.x), it was the most controversial version in Python’s history, but it also shed the heavy burdens accumulated over the years. Since then, Python has moved forward with a lighter footprint. Starting from version 3.6, it became the first relatively stable and reliable version of the Python 3 series. During this process, with the rapid evolution of big data, machine learning, and artificial intelligence, Python further leveraged its advantages, gaining recognition and usage by more people.

Python is an elegant, charming, easy-to-learn, and efficient development language. From the beginning, it prioritized readability, natural language proximity, and ease of development, returning the joy of programming to developers. In 1999, founder Guido Van Rossum initiated a movement called CP4E (Computer Programming for Everybody), aiming to enable almost everyone to write and improve computer programs. The manifesto for this movement is available here[^CP4E]. It states that several years ago, Xerox proposed the grand vision of having a computer on every desktop, a vision that has since been realized. However, computers were not flexible enough. What if everyone had the ability to program their computers?

One of the goals of this movement was to design a programming language course for middle school students. We see that many provinces in China have now begun requiring middle school students to learn Python programming. It can be said that the philosophy of this movement has subtly gained global recognition. In fact, it is precisely Python’s concise elegance, natural language proximity, and interpretation-based nature (no compilation required) that made the CP4E goal achievable.

If "elegance and charm" is somewhat subjective, as every person’s ideal may differ, few would deny Python’s simplicity and efficiency. "Life is short, use Python" is not just a slogan but a true reflection of Python’s high development efficiency.

Compared to other development languages, Python code is consistently the simplest and most readable when implementing the same functionality without relying on external libraries. Comparing C, Java, and Python, Java has the largest code volume, being 1.5 times longer than C and 3–4 times longer than Python. Let us experience this by outputting the elements of an array.

This is the Python example:

```python
arr = ["Hello, World!", "Hi there, Everyone!", 6]
for i in arr:
    print(i)
```

This is the Java example:

```Java
public class Test {
    public static void main(String args[]) {
        String array[] = {"Hello, World", "Hi there, Everyone", "6"};
        for (String i : array) {
          System.out.println(i);
        }
    }
}
```

Looking only at the definition and the output of array elements, both languages require three lines of code, but Python’s code is clearly shorter. Moreover, Python offers so-called "pythonic" approaches:

```python
[print(i) for i in ["Hello, World!", "Hi there, Everyone!", 6]]
```

Of course, writing it this way is still controversial; for some, it sacrifices readability.

Let us look at another example: variable swapping.

```c
// C program to swap two variables in single line
#INCLUDE <STDIO.H>
int main()
{
	int x = 5, y = 10;
	//(x ^= y), (y ^= x), (x ^= y);
    int c;
    c = y;
    y = x;
    x = c;
	printf("After Swapping values of x and y are %d %d", x, y);
	return 0;
}
```

```Java
class GFG {
	public static void main(String[] args)
	{
		int x = 5, y = 10;
		//x = x ^ y ^ (y = x);
        int c;
        c = y;
        y = x;
        x = c;
		System.out.println("After Swapping values"+" of x and y are " + x + " " + y);
	}
}
```

```python
x, y = 5, 10
x, y = y, x
print("After Swapping values of x and y are", x, y)
```

Python’s syntax is clearly simpler. It resembles the natural language we use daily, seemingly requiring no complex techniques or even knowledge of programming concepts to achieve these functions. While C and Java can also swap variable values in one line without a third variable, such code requires specific techniques and is prone to errors.

Concise code (without requiring complex techniques) is clearly easier to read and understand, significantly accelerating development speed. Indeed, in this era of information overload, simplicity is showing powerful strength: JSON has replaced XML as the preferred tool for data transmission; Markdown has replaced HTML, reStructuredText, and Word as our document format.

"Trimming the繁复 in autumn trees, creating the new in February flowers." Cumbersome, exaggerated Baroque art, no matter how exquisite or eye-catching, cannot escape criticism in this highly competitive era. We need tools, symbols, and ideas that become our intuition, allowing us to respond quickly to an increasingly complex world.

!!! note
    Simplicity is beauty. This philosophical thought roughly originated with Ockham. Da Vinci had a similar idea: "Simplicity is the ultimate sophistication," although sophistication was the aesthetic of Da Vinci’s time. If you are interested in these thoughts, you can further read John Maeda’s book, *The Laws of Simplicity*.

The importance of language simplicity and elegance in Python is so significant that it is written into Python’s "charter" -- PEP20[^PEP20]:

!!! Cite 
    "Zen of Python - by Tim Peters[^Tim_Peters]"   
      
    Beautiful is better than ugly.
    优美胜于丑陋

    Explicit is better than implicit.
    明了胜于晦涩

    Simple is better than complex.
    简单优于复杂

    Complex is better than complicated.
    复杂优于凌乱

    Flat is better than nested.
    扁平好过嵌套

    Sparse is better than dense.
    稀疏强于稠密

    Readability counts.
    可读性很重要！

    Special cases aren't special enough to break the rules.
    特例亦不可违背原则

    Although practicality beats purity.
    即使实用战胜了纯粹

    Errors should never pass silently.
    错误绝不能悄悄忽略

    Unless explicitly silenced.
    除非我们确定需要如此

    In the face of ambiguity, refuse the temptation to guess.
    面对不确定性，拒绝妄加猜测

    There should be one -- and preferably only one -- obvious way to do it.
    永远都应该只有一种显而易见的解决之道

    Although that way may not be obvious at first unless you're Dutch.
    即便解决之道起初看起来并不显而易见

    Now is better than never.
    做总比不做强

    Although never is often better than *right* now.
    然而不假思索还不如不做

    If the implementation is hard to explain, it's a bad idea.
    难以名状的，必然是坏的

    If the implementation is easy to explain, it may be a good idea.
    易以言传的，可能是好的

    Namespaces are one honking great idea -- let's do more of those!
    名字空间是个绝妙的主意，请好好使用！

This text even appears as an easter egg. If you execute the following command:

```bash
python -c 'import this'
```

it will output the text above. Whenever I need to quote the *Zen of Python*, I use this method.

PEP20 hides another easter egg. We say it should have 20 rules, but we can only see 19. Why?

Actually, the 20th rule is Guido’s privilege. For years, the community has waited for him to add this rule. This also reflects the community’s respect and love for Guido. However, over 10 years have passed, and to date, Guido has not used this privilege. Thus, this 20th "military rule" remains vacant.

Secondly, Python’s efficiency is reflected in its ability to run without compilation. In compiled languages like C and Java, if you write a small program and want to see how it runs, you must wait for it to compile -- this time could be tens of seconds, minutes, or even hours -- which interrupts the programmer’s workflow. The following satirical cartoon reflects this situation:

![50%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/202106/27ed4c0b74066c8bb0ab8b5bfb2afe88_1440w.png)

In Python, you can open its interactive interface (i.e., IPython) at any time, input a small piece of code, and immediately see the result. The following image shows how to calculate mathematical problems in the IPython interface:

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/202105/20210522232747.png)

If you do not like using IPython’s command-line interface, you can install Jupyter Notebook to write and run Python code snippets. We will introduce Jupyter Notebook further when discussing IDEs. Additionally, writing a quick Unittest to test your newly written methods is easier in Python than in other languages. Thus, using Python, you will find learning and growth so easy!

Finally, Python’s ability to become an efficient development language is also due to its vast and active community. In the Python world, you can easily find pre-built "wheels," making building your applications as simple as stacking blocks. For example, if you sometimes need to display HTML-formatted documents or present local files for download via the Web, you can start an HTTP server as simply as below:

```bash
python -m http.server
```

This starts a web server that lists the directory of the folder where the command was launched, without requiring you to install or configure any software!

Fame brings criticism. As a programming language suitable for everyone, Python bears hopes while also应承担ing many doubts. The loudest of these doubts concern Python’s performance and its ability to build large, complex applications.

Indeed, compared to other development languages, Python lags significantly in execution speed. To some extent, this lag is intentional, as for a long time, Python’s creator did not believe that excessive attention needed to be paid to Python’s performance, as it was already fast enough. Indeed, for over 99% of tasks, Python’s performance is sufficient, fast enough to support early Google and Dropbox -- application scenarios that many programmers encounter only once in a lifetime. Since then, Python has made substantial progress in performance. The release of ChatGPT in 2023 -- whose high-performance computing backend is implemented by the Ray library in Python[^Ray] -- not only tells us how advanced AI language models can be but also that Python can be used to build high-performance, highly scalable large-scale distributed computing platforms. Currently, this platform supports over 100 million monthly active users, and we do not yet know where its bottlenecks lie. Therefore, we can no longer say that Python is unsuitable for building large applications.

However, there are reasons to demand faster execution from Python. After all, regardless of how powerful the computing platforms built with Python are, Python’s single-process computing power is still slower than many other languages in many scenarios. If Python itself runs slowly, and if the application architecture is poorly designed, performance bottlenecks may still occur -- it should be noted that poor application architecture is the cause of performance bottlenecks in the vast majority of applications, and the development language should not be blamed. For example, many people criticize Python’s GIL (Global Interpreter Lock) for preventing full utilization of multi-threading advantages. In reality, using multi-threading in programs is often a bad idea; you should use Coroutines and multi-processing instead, which often achieves better performance.

However, in the near future, we will no longer need to worry about Python’s performance: at the Python Developers Summit in May 2021, Guido announced a plan to improve Python’s performance by five times or more over the next four years. Let us imagine: by then, will Ray become one of the most powerful computing platforms in the world?

Another question is whether Python is suitable for developing large, complex applications. If the doubts about Python’s performance have factual basis, this doubt only reflects the questioner’s lack of understanding of Python’s development. Specifically, these doubts are: first, Python’s dynamic typing makes type inference difficult, which is unfavorable for static code checking and refactoring; second, since Python code has no compilation process, it lacks the mechanism for discovering errors at compile time.

Regarding the first doubt, Python introduced type annotations starting from version 3.3, and by Python 3.8, a basic system was formed. Therefore, as long as code is written according to standards, type inference and code refactoring are not problems. JavaScript is a vivid example; it is also a dynamic language, but after introducing type hints, it upgraded to TypeScript, which is now very successful. Regarding the second point, compile-time checking is only one way to enhance code quality, not the only one. The only standard for testing code quality is whether it meets your expectations at runtime. This is exactly what unit tests and integration tests do. Due to Python’s dynamic typing, building Mock objects is very simple, making unit testing exceptionally easy. This encourages programmers to conduct more sufficient and comprehensive unit tests, thereby greatly improving code quality.

Therefore, in the author’s view, the reason some people doubt Python’s ability to develop large applications is more because they do not understand or are familiar with Python’s software development processes, standards, and tools. In fact, if you follow Python’s best practices for software development, make good use of standards and tools, developing large applications with Python can significantly shorten development time, improve development efficiency, and make commercial success more attainable.


<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official copy of this book</a>
</div>
</div>


[mars-rover-space-traveler]: https://pixabay.com/photos/mars-mars-rover-space-travel-rover-67522/

[^Java]: Java version 1.0 was released in January 1996. Python was created in February 1991.
[^PEP20]: PEP stands for Python Enhancement Proposals. It is an important way to introduce new features into Python.
[^Tim_Peters]: Tim Peters is one of Python’s important contributors and the inventor of the Timsort sorting algorithm, which is widely used in various languages including Python, such as the Chrome V8 engine and Node.js.
[^Dropbox]: Dropbox initially used Python 2.x. Dropbox eventually rewrote some features using other languages because many believed that upgrading from Python 2 to Python 3 was akin to changing languages.
[^CP4E]: CP4E Movement: https://www.python.org/doc/essays/cp4e/
[^TIOBE]: https://www.tiobe.com/tiobe-index/
[^ray]: ChatGPT’s demand for computing power is astonishing. Therefore, they used Ray, a shared-memory distributed computing platform written in Python. Ray’s developers are Anyscale, co-founded by several professors from UC Berkeley and co-founders of Databricks.
