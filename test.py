from fasthtml.common import *
count = 0

app, rt = fast_app()
@rt("/")
def get():
    return Titled("计数器",
        Div(
            H1(f"当前计数: {count}"),
            # 点击按钮时，向 /increment 发送 POST 请求
            # 并将返回的内容替换掉 id 为 'counter' 的元素
            Button("点我 +1", hx_post="/increment", hx_target="#counter", hx_swap="innerHTML"),
            id="counter"
        )
    )

@rt("/increment")
def post():
    global count
    count += 1
    # 只返回更新后的部分 HTML
    return Div(
        H1(f"当前计数: {count}"),
        Button("点我 +1", hx_post="/increment", hx_target="#counter", hx_swap="innerHTML")
    )

serve()
