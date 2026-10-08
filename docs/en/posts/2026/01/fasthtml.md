---
title: "FastHTML: The 2026 Frontend Standard for Quant Systems"
date: 2026-01-11
slug: en/posts/tools/2026十大量化技术/fasthtml
tags: [FastHTML, Quantitative Trading, Python Web Development, HTMX]
excerpt: "FastHTML replaces Streamlit’s limitations with HTMX and Starlette, enabling high-performance, interactive quant frontends using pure Python. This article details the architecture and benefits for 2026 quant infrastructure."
lang: en
translation_of: posts/tools/2026十大量化技术/fasthtml
auto_translated: true
source_sha: bce87058ec0b61e40b9086e2cca22e5f5dff12f0
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/20260110212357.png"
---

This is the third article in the "2026 Quantitative New Infrastructure" series. Our goal is to introduce the technologies you might (and should) use to build a quantitative trading system in 2026. Today, we focus on the technologies you should use to build the frontend of a quantitative trading system in 2026.

<div style='width:80%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/20260110212357.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>Australian National University, Parabolic Solar Concentrator</span>
<span style='font-size:0.7em;display:inline-block;width:100%;text-align:center;color:grey'>by Toby Hudson@wikimedia</span>
</div>

On the internet, people or companies that provide free resources and services are often called "Cyber Lamas." The most famous Cyber Lama is undoubtedly Cloudflare. However, I would also like to call Jeremy Howard, the founder of fast.ai, a Cyber Lama, because he has developed a series of software products starting with "fast," such as fastai, fastlite, and fasthtml.

Time is one of the few resources that everyone possesses fairly. In this sense, if a technology can improve time efficiency, I believe it deserves to be called a Cyber Lama.

This is exactly why we should embrace FastHTML.

However, to truly understand the revolutionary nature of FastHTML, we first need to look back at who the current ruler of this field is, and why it is not yet perfect.

## The Former King: Streamlit

Streamlit was founded by Adrien Treuille (CEO), Thiago Teixeira, and Amanda Kelly. All three founders previously worked at Google X.

Adrien Treuille was a computer science professor at Carnegie Mellon University. During his time at Google X, he deeply understood the pain points faced by data scientists: as data scientists (quantitative strategy researchers can relate), their native language is Python, but Python cannot be used to build web applications. Consequently, they cannot independently build even the simplest data applications.

To build a web application with a perfect interactive experience, you need to master technologies such as HTML, CSS, JavaScript, TypeScript, React, and Vue.js. This has always been the exclusive domain of frontend engineers.

Treuille and his colleagues decided to develop a web framework based entirely on Python. Unlike the Python web frameworks we are familiar with, such as Django and Flask, it not only has web server functionality but, more importantly, frontend components can also be built using only Python objects or even Markdown text. As a result, you barely need to master frontend knowledge.

Before Streamlit was born, there were already some similar solutions on the market, such as Plotly Dash, which we introduced in our "Quant 24 Lessons." Plotly Dash is very powerful and flexible. However, **complexity is the tax on flexibility**, and Plotly Dash’s learning curve is not gentle.

This gave Streamlit the opportunity to break out. With extreme simplicity, Streamlit successfully lowered the threshold for developing web applications to nearly zero, becoming the preferred tool for Python data scientists to showcase their work. To date, it has garnered 43k stars on GitHub and was acquired by Snowflake for $800 million in 2022.

![Quantitative program developed using Streamlit](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/20260110174624.png)

Streamlit’s success was phenomenal, much like *Zootopia* in its year. It swept the field with its perfect setting upon release. Facing such a classic that has already been deified, you might harbor doubts, just as you now view *Zootopia 2*: Is there really room to tell new stories in this track when there is already a pearl of excellence? Do latecomers still have a chance to surpass the ceiling left by the predecessor?

In fact, there is no final outcome in the world of technology. Streamlit development is indeed fast, but once your application becomes successful, you will likely have to rewrite it to support tens of thousands of users and meet their demands for extreme interactive experiences.

Jeremy Howard, the founder of fast.ai, saw this point. He arrived with FastHTML, trying to tell us: Python programmers should not have to choose between "simplicity" and "power." We can have both.

## The Uncompromising FastHTML

Streamlit’s extreme simplicity comes at the cost of flexibility and performance. Web pages created with Streamlit inevitably suffer from a "one-size-fits-all" feel, and some interactive scenarios cannot be implemented. Additionally, there are deficiencies in performance.

FastHTML has none of these problems, thanks to its foundation on two excellent frameworks: Starlette and HTMX.

Starlette is a lightweight Python web framework based on the ASGI protocol. It is also the core cornerstone of the currently most popular FastAPI. Simply put, **FastAPI = Starlette + Pydantic (data validation) + OpenAPI (automatic documentation)**. Professor Jeremy Howard’s **FastHTML**, on the other hand, is **Starlette + HTMX + Python Component System**. It uses Starlette to ensure high backend performance, introduces HTMX to solve frontend interaction without writing JS, and encapsulates HTML tags as Python objects, allowing developers to build modern web applications using pure Python.

For most Python developers, Starlette is already an old friend. It is the solid foundation of FastAPI, known for its high performance and stability. We will not elaborate here.

What truly gives FastHTML the magic of "turning stone to gold" is **HTMX**.

## The Core of Magic: HTMX

If you are a typical backend developer, you may detest the complexity of the frontend: to update part of a page with a button, you have to introduce React/Vue, configure Webpack, and write backend APIs for joint debugging.

HTMX appeared to end this nightmare. It allows you to drive modern interactions directly using attributes (attributes) in HTML tags.

For example, traditional HTML can only initiate requests via `<a>` and `<form>`. HTMX allows any element (such as `<div>`, `<button>`) to initiate HTTP requests (GET, POST, PUT, DELETE) and directly replace part of the page with the HTML fragment returned by the server.

This means, **you no longer need to write JavaScript to handle frontend-backend communication and DOM updates**. All logic returns to your most familiar Python backend.

This is precisely the essence of FastHTML. It leverages Python’s expressiveness to encapsulate HTML tags into Python objects (components). When the code runs, these objects are "compiled" into standard HTML with HTMX attributes. This means you can easily define page components that support **partial refreshing** using pure Python code.

In comparison, Streamlit’s design philosophy is "once there is interaction, rerun the entire script (Rerun)." While this mechanism is simple, it appears cumbersome when handling complex interactions. Although Streamlit finally launched the `st.fragment` decorator in version **1.37.0** (mid-2024) to attempt similar partial refreshing functionality, compared to FastHTML’s design based on "components + partial exchange" from the ground up, the former looks like a belated patch, while the latter is a native, high-performance engine.

## The Hot New Star

This philosophy of "returning to simplicity" is sweeping the entire development community.

*   **HTMX**: It is already the "hot new chicken" in the frontend field. In the 2024 JavaScript Rising Stars评选, HTMX’s GitHub Star growth even exceeded that of React and Vue, with its total star count currently breaking through **44k**. It represents a reflection: perhaps we don’t need such complex JS frameworks.
*   **FastHTML**: As the best partner for HTMX in the Python world, although it was just released in **August 2024**,凭借 Jeremy Howard’s appeal and pain-point-driven design, it captured over **6.6k** stars on GitHub within just a few months (as of early 2026).

This is not just a combination of two libraries, but a movement of "de-complexification." "Trimming the autumn tree to its essence, creating new styles in February flowers." FastHTML achieves both simplification and innovation.

## FastHTML Quick Start

FastHTML’s design philosophy is "explicit is better than implicit," while maintaining extreme simplicity. You do not need to configure route tables, set up template directories, or even manually start the server (if you use `serve()`).

### 1. Hello, World!

Let’s look at the smallest FastHTML application:

```python
from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def get():
    return Titled("FastHTML Demo", 
        Div(
            H1("Hello, World!"),
            P("This is my first FastHTML application")
        )
    )

serve()
```

Running this code starts a complete web server. Here are a few key points:
*   **`fast_app()`**: Initializes the application, returning the `app` object and the route decorator `rt`.
*   **Python Components**: `Div`, `H1`, `P` are all Python classes. You no longer need to manually write tags like `<p>...</p>`; instead, you build pages using Python objects like building blocks. This not only avoids spelling errors but also allows you to enjoy IDE auto-completion.

### 2. Adding Interaction (HTMX)

The current page is static. Let’s add some "magic" and create a counter without JS:

```python
from fasthtml.common import *
count = 0

app, rt = fast_app()
@rt("/")
def get():
    return Titled("Counter",
        Div(
            H1(f"Current Count: {count}"),
            # When the button is clicked, send a POST request to /increment
            # and replace the element with id 'counter' with the returned content
            Button("Click Me +1", hx_post="/increment", hx_target="#counter", hx_swap="innerHTML"),
            id="counter"
        )
    )

@rt("/increment")
def post():
    global count
    count += 1
    # Return only the updated part of the HTML
    return Div(
        H1(f"Current Count: {count}"),
        Button("Click Me +1", hx_post="/increment", hx_target="#counter", hx_swap="innerHTML")
    )

serve()
```

In this example:
1.  `hx_post="/increment"`: Tells the frontend to send a POST request to `/increment` when the button is clicked.
2.  `hx_target="#counter"`: Tells the frontend to find the element with `id="counter"` on the page after receiving the server’s response.
3.  `hx_swap="innerHTML"`: Replaces the content inside the target element with the returned content.
   
![SPA application generated by FastHTML](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/20260110213304.png)

The entire process involves **not a single line of JavaScript**. It is incredibly concise, yet the user experience is a seamless, single-page application (SPA)-level experience without page refreshes.

## Jeremy’s "Personal Imprint"

If you are familiar with Jeremy Howard, the founder of fast.ai, you will find that every design detail of FastHTML is deeply marked with his personal philosophy: **pragmatism** and **exploratory programming**.

### 1. Writing Web Apps Like Data Analysis (nbdev DNA)

Jeremy is a fervent believer in **Jupyter Notebooks**. He even developed the `nbdev` system, advocating for the development of production-level code directly in Notebooks. He believes that programming should not be a cycle of "write code blindly -> start service -> refresh browser," but rather a process of **real-time interaction and feedback**.

FastHTML perfectly inherits this DNA. You can define routes and write components directly in Notebook cells, then call `serve()`. The application runs directly in the Notebook output area, supporting hot reloading.

This means web development can finally be like data analysis: write a line of code, and immediately see the result. For Python developers accustomed to the REPL experience, this "exploratory programming" thrill is irresistible.

### 2. Born for the AI Era (AI-First)

As a top AI expert, Jeremy knows better than anyone that **in 2024, if a new framework cannot be mastered by AI, it has no future.**

Because FastHTML is too new, large models like ChatGPT know nothing about it. Jeremy did not wait for models to retrain; instead, he took the initiative to establish the **`llms.txt`** standard and provided a dedicated "AI knowledge capsule" for FastHTML: `/llms-ctx.txt`.

This reflects his consistent pragmatic style: **not only to make it feel good for humans, but also to make it understandable for AI.** You only need to feed this file to Cursor or Claude, and they instantly transform into FastHTML experts. This "AI-native" documentation design may become the standard for all future open-source projects.

## What About Aesthetics?

This is a very realistic issue. For a long time, web applications built by Python developers (such as early Streamlit or Gradio) always had a "rough engineering" feel, making it difficult to achieve commercial-grade aesthetics.

FastHTML has prepared two hands for this:

**High Floor (Pico CSS)**: By default, FastHTML automatically enables **Pico CSS**. This is a minimalist CSS framework that does not require you to write any classes, yet it gives standard HTML elements (buttons, forms, tables) a modern, clean appearance and automatically supports dark mode. This means that even if you know nothing about CSS, the applications you write will be "presentable."

**Unlimited Ceiling (Tailwind CSS, etc.)**: If you have extreme pursuit of aesthetics, the essence of what FastHTML generates is standard HTML, so it is compatible with all CSS ecosystems. Therefore, you can directly use **Tailwind CSS** (currently the most popular atomic CSS framework) to customize every pixel. At the same time, you can introduce any third-party CSS libraries or custom style sheets.

## Conclusion: Let Technology Return to Service

FastHTML’s official website is [fastht.ml](https://fastht.ml), where you can find more examples and documentation.

---

Thus, our **"2026 Quantitative New Infrastructure"** series has introduced three pieces of the puzzle:

1.  **uv & Pydantic**: Using ultra-fast package management and strict data validation to consolidate the **engineering foundation**.
2.  **SQLite (WAL)**: Using a high-performance, single-file database that requires no maintenance to solve the pain points of **data storage**.
3.  **FastHTML**: Using a pure Python web framework to bridge the last mile of **interaction and presentation**.

The common feature of these technology selections is: **anti-involution, emphasis on practical results**. They do not pursue "large and comprehensive" enterprise-level architectures, but are dedicated to allowing individual developers and small teams to build high-performance, highly available quantitative systems with the minimum cognitive burden.

In 2026, the threshold for technology should be flattened, not built higher. I hope this set of "new infrastructure" can liberate you from tedious infrastructure work, allowing you to invest your most valuable energy into the mining of Alpha.
