---
title: "Dash Web Apps: Routing, Auth, and Pitfalls"
date: 
slug: en/articles/python/visualize/dash
tags: [Dash, Web Development, Routing, Authentication]
excerpt: "Explore Dash’s core concepts, routing strategies, and authentication patterns. Learn to build scalable, multi-page Python web apps while avoiding common pitfalls in layout management and state handling."
lang: en
translation_of: articles/python/visualize/dash
auto_translated: true
source_sha: 44158dcc5ee96af74b363912088884c91ba5e89f
---

# Dash Web Apps: Core Concepts, Routing, Auth, and Pitfalls

Dash is a framework for developing web interfaces using Python. It compiles frontend code into HTML/JS/CSS at runtime, enabling Python developers to function as full-stack engineers. Its key features include:

1. **Pure Python Development:** Both UI elements and server-side logic are written entirely in Python. Dash handles the conversion of Python UI components into HTML/JS/CSS and manages frontend-backend interactions. This allows developers to complete all tasks within the Python ecosystem.

2. **Built-in Flask Server:** Dash includes a Flask server, meaning many Flask mechanisms apply. For example, you can access cookies as shown below:

```python
import flask

flask.request.cookies.get("your cookie name")
```

This code can be used globally or within a `callback` method (specifically `app.callback` in Dash).

3. **Seamless Plotly Integration:** Dash offers strong visualization capabilities. Notably, these visualizations are web-interactive yet programmed entirely in Python (unlike JavaScript, which provides interactivity natively).

This article summarizes our experience with Dash, covering core concepts, routing, authentication, and common pitfalls.

I am Quant Fengyun, a quantitative practitioner with years of experience in quantitative framework and strategy development. Follow for more! For localized deployment of quantitative research frameworks, consider [Zillionare 2.0](https://blog.quantide.cn). Built on InfluxDB, it currently stores over 3.5 billion market data records in production environments.

## 1. Core Concepts

In traditional web programming, we typically prepare two handlers for a view: one for GET requests to provide the initial interface for user interaction, and another for POST requests to receive submitted data, process it, and redirect to a new view.

In Dash, this interaction is invisible to the user. We prepare a single view and use `callback` to handle user input. When users interact with the frontend, Dash automatically forwards these messages (click events or value changes) to the backend. The application retrieves these input values in the `callback`, performs validation, and updates specific controls within the same view or renders a new view (if the `Output` is bound to the `children` property of an HTML control).

```python
layout = dbc.Container(
    [
        html.Br(),
        dbc.Container(
            [
                dcc.Location(id="urlLogin", pathname="/login", refresh=True),
                html.Div(
                    [
                        dbc.Container(
                            html.Img(
                                src="/assets/dash-logo-stripe.svg", className="center"
                            ),
                        ),
                        dbc.Container(
                            id="loginType",
                            children=[
                                dcc.Input(
                                    placeholder="Enter your username",
                                    type="text",
                                    id="usernameBox",
                                    className="form-control",
                                    n_submit=0,
                                ),
                                html.Br(),
                                dcc.Input(
                                    placeholder="Enter your password",
                                    type="password",
                                    id="passwordBox",
                                    className="form-control",
                                    n_submit=0,
                                ),
                                html.Br(),
                                html.Button(
                                    children="Login",
                                    n_clicks=0,
                                    type="submit",
                                    id="loginButton",
                                    className="btn btn-primary btn-lg",
                                ),
                                html.Br(),
                            ],
                            className="form-group",
                        ),
                    ]
                ),
            ],
            className="jumbotron",
        ),
    ]
)

################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - REDIRECT TO PAGE1 IF LOGIN DETAILS ARE CORRECT
################################################################################
@callback(
    Output("urlLogin", "pathname"),
    Input("loginButton", "n_clicks"),
    [State("usernameBox", "value"), State("passwordBox", "value")],
    suppress_callback_exceptions=True,
)
def on_login(n_clicks, username, password):
    if n_clicks == 0:
        print("first loaded")
    else:
        print("login button clicked with:", username, password)
        response = dash.callback_context.response
        if login_user(response, username, password):
            # JUMP TO INDEX PAGE
            return "/"

@callback(
    Output("usernameBox", "className"),
    [
        Input("loginButton", "n_clicks"),
        Input("usernameBox", "n_submit"),
        Input("passwordBox", "n_submit"),
    ],
    [State("usernameBox", "value"), State("passwordBox", "value")],
)
def update_output(n_clicks, usernameSubmit, passwordSubmit, username, password):
    print("update_output by usernameBox")
    if (n_clicks > 0) or (usernameSubmit > 0) or (passwordSubmit > 0):
        if get_current_user() is None:
            response = dash.callback_context.response
            if login_user(response, username, password):
                return "form-control"
            else:
                return "form-control is-invalid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"

################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF LOGIN DETAILS INCORRECT
################################################################################
@callback(
    Output("passwordBox", "className"),
    [
        Input("loginButton", "n_clicks"),
        Input("usernameBox", "n_submit"),
        Input("passwordBox", "n_submit"),
    ],
    [State("usernameBox", "value"), State("passwordBox", "value")],
)
def update_output(n_clicks, usernameSubmit, passwordSubmit, username, password):
    print("in update_output: passwordBox")
    if (n_clicks > 0) or (usernameSubmit > 0) or (passwordSubmit) > 0:
        if get_current_user() is None:
            response = dash.callback_context.response

            if login_user(response, username, password):
                return "form-control"
            else:
                return "form-control is-invalid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"

```

The code above defines a view. Note the following:

1. The view contains a `dcc.Location` object. Its presence allows us to modify its `url` property via a `callback`, triggering a page reload (either the current view or a new page).

2. In the first `callback`, we receive values from `usernameBox` and `passwordBox` to determine if the user can log in. If allowed, we update the `dcc.Location` object’s path to `"/"`. This path points to the application’s default display page (the homepage). This is achieved by binding the two input controls (and `loginButton`) as inputs and the `urlLogin` control (`dcc.Location`) as the output, returning the path `"/"` upon success.

3. The other two methods handle cases where input validation fails, prompting the user about which control has errors. We do not modify the `pathname` of the `urlLogin` control, so the user remains on the current page.

## 2. Routing

Generally, Dash applications do not have routing. However, building large-scale applications inevitably involves routing. In traditional C/S programs, features are organized into pages (each corresponding to a URL), and the server generates response pages based on routing configurations triggered by browser-submitted paths.

In large Single Page Applications (SPAs), even if the server handles only a few routes, we often generate a routing table on the frontend to switch views, keeping code concise and readable (another reason is to enable lazy loading, improving initial response speed).

Clearly, building complex Dash applications requires routing. Dash does not currently provide a frontend routing mechanism; instead, it offers a multi-page application approach. The core idea is that once the current view is processed, it can modify the `pathname` attribute of the `Location` control in the page (via the `callback` mechanism, as described in the previous section), triggering a redirection.

Below is a simple routing implementation.

First, we define a `layout` following Dash conventions:

```python
# ROUTING.PY

layout = html.Div(
    [
        dcc.Location(id="router", refresh=False),
        html.Div(id="page-content")
    ],
    id="rootElement",
)
```

This layout is simple because we do not intend to display anything here; it serves solely for routing forwarding. To achieve this, we need a mechanism to modify the `pathname` attribute of the `url` `Location` control (assuming all jumps occur within the same service). This is done by binding this control as an `Output` and the `Location` control as an `Input`:

```python
# ROUTING.PY

@callback(Output("page-content", "children"), 
          [Input("router", "pathname")])
def _routing(pathname):
    # ENSURE AUTH
    if not auth.get_current_user():
        return auth.layout

    handler = routes.get(pathname, None)
    if handler is None:
        return homepage.layout

    return handler()
```

The `Location` control is special; it does not appear in the page elements. Although a page may allow multiple `Location` controls, they all update the current window’s address.

The mechanism for the above `callback` is as follows: when the current window’s `pathname` (Dash terminology for the `server_path` in `http://host:port/server_path?query_string`) changes, this `callback` is triggered, and the function receives the new `pathname`. Here, we check if the user is logged in. If not, we return the login page (`auth.layout`). Otherwise, we call the event handler corresponding to the path. Typically, the event handler returns a new page view, which Dash loads into the `page-content` element mentioned above. The original elements in `page-content` are cleared (which may cause memory issues).

There are no actual routing or routing handler functions visible here. All routes are collected in the `routes` set in `routing.py`, and we provide a decorator for components to register their routes themselves:

```python
# ROUTING.PY

routes = {}

def on(pathname: str):
    """
    dispatch function.
    """
    def decorator(func):
        global routes

        routes[pathname] = func
        return func
    return decorator
```

The `auth` view is slightly more complex. The part related to routing is:

```python
layout = dbc.Container(
    [
        html.Br(),
        dbc.Container(
            [
                dcc.Location(id="urlLogin", pathname="/login", refresh=True),
              ...
              
# CALLBACK
@callback(
    Output("urlLogin", "pathname"),
    Input("loginButton", "n_clicks"),
    [State("usernameBox", "value"), State("passwordBox", "value")],
    suppress_callback_exceptions=True,
)
def on_login(n_clicks, username, password):
    if n_clicks == 0:
       ...
```

In the code above, clicking `loginButton` or changing the values of `usernameBox` and `passwordBox` triggers this `callback`. When called, we already have the user-entered `username` and `password` (bound to `Input` and `State` objects in declaration order). We then check if the `username` and `password` are valid. If valid, we log the user in, generate a session, and finally return a path (string). Dash updates this path in the `Location` control, causing Dash to request the new page from the backend.

### Registering Routes

In the `controller.py` of the `auth` module, we register two routes:

```python
from .models import get_current_user, remove_current_user
from .view import layout
from alpha.web import routing

@routing.on('/logout')
def logout():
    if  get_current_user():
        remove_current_user()

    return layout

@routing.on('/login')
def login():
    return layout
```

When `controller.py` is imported, registration occurs automatically. However, we need a method to ensure this registration completes before the program starts. Therefore, `routing` provides a `build_blueprints()` method:

```python
def build_blueprints():
    """
    collect all routes by import controller from web/*/controller.py
    """
    _dir = os.path.dirname(os.path.abspath(__file__))
    package_prefix = "alpha.web."
    for pyfile in glob.glob(f"{_dir}/**/controller.py"):
        sub = pyfile.replace(f"{_dir}/", "").replace(".py", "").replace("/", ".")
        module_name = package_prefix + sub
        importlib.import_module(module_name)
```

This method requires all page modules to be placed in the `alpha.web` directory, with event handlers in `controller.py`. If your code has a different organization, you need to modify this.

Let’s look at another view: the root view. After logging in, users enter this view. Located under `alpha.web.homepage`, its view is particularly simple:

```python
from dash import html, dcc, callback, Input, Output
from alpha.web import auth

layout = html.Div(
    [
        dcc.Location(id="homepage", refresh=False)
        html.H1("logout"),
        dcc.Link("Logout", href="/logout"),
    ], id="rootElement"
)

```

It provides a link that, when clicked, redirects to the `/logout` path (another method in Dash to change views). The `routing` module then detects the new `pathname`, triggers the `callback`, finds the `/logout` handler, logs out the current user, and redirects to the login page. Thus, the `Location` component here does not play a direct role; we declare it for future use.

## 3. Gotchas

The key reason `routing.py` can provide routing is that `rootElement` is the parent node for all subsequent views. As long as this node exists, the routing mechanism is effective.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/07/dash-gotcha.jpeg)

As shown in the image above, even when switching to the `logout` view, this `rootElement` still exists. Therefore, in `routing`, we must update new views under the `page-content` node, not under `rootElement`. Otherwise, we would destroy the global routing.
