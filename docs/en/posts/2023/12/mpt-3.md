---
title: "Portfolio Optimization: Convex Optimization for Efficient Frontiers"
date: 2023-12-13
slug: en/articles/investment/策略研究/mpt-3
tags: [Portfolio Optimization, Convex Optimization, SciPy, Efficient Frontier]
excerpt: "Leverage SciPy’s minimize function to solve constrained portfolio optimization problems, constructing efficient frontiers by balancing target returns against volatility and Sharpe ratio constraints."
lang: en
translation_of: articles/investment/策略研究/mpt-3
auto_translated: true
source_sha: 8f1f91961506123f529d52a05c36de4027ed6730
---

Finding the minimum volatility for a given return, or the maximum Sharpe ratio for a given volatility, represents a common class of optimization problems:

![Mathematical formula for optimal portfolio solution: minimizing volatility under constraints](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/mpt-optimize-formula.png)

We can use the `scipy.optimize` library to solve such problems.

**Main Features of the scipy.optimize Package**
* SciPy Optimize provides functionality to minimize (or maximize) an objective function, potentially subject to constraints.
* It includes solvers for nonlinear problems (supporting local and global optimization algorithms), linear programming, constrained and unconstrained least squares, root finding, and curve fitting.
* When optimizing input function parameters, `scipy.optimize` offers various useful methods capable of handling different types of functions.

It provides the following methods:
* `minimize_scalar()`: Minimizes a single-variable function.
* `minimize()`: Minimizes a multi-variable function.
* `curve_fit()`: Finds the optimal curve fitting a set of data.
* `root_scalar()`: Finds the root of a single-variable function.
* `root()`: Finds the roots of multi-variable functions.
* `linprog()`: Minimizes a linear objective function subject to linear equality and inequality constraints.

Among these methods, we will primarily focus on **`minimize_scalar`** and **`minimize`**.

### minimize_scalar

For problems where the solution is a single number, such as solving an equation, the `minimize_scalar` method can be used.

For example, consider our function:

$y=3x^4-2x+1$

`minimize_scalar()` helps us find the precise coordinates where the function reaches its minimum value (minimum $y$). In plain terms, this is equivalent to solving the equation.

```python
from scipy.optimize import minimize_scalar

def objective_function(x):
    return 3 * x ** 4 - 2 * x + 1
# 定义需要求解的函数

res = minimize_scalar(objective_function)
# 求出函数的最小值

print(res)
```

Let’s focus on interpreting the output, which we will use repeatedly later:

```
 message: 
          Optimization terminated successfully;
          The returned value satisfies the termination criteria
          (using xtol = 1.48e-08 )
 success: True
     fun: 0.17451818777634331
       x: 0.5503212087491959
     nit: 12
    nfev: 15
```

Here, `fun` represents the function value, and `x` represents the variable value. If we substitute the value of `x` into the formula $3x^4-2x+1$, we obtain 0.17, which matches the value of `fun`.

Note that optimization is not always possible. For instance, $y=x^3$ has no minimum value; attempting to optimize it would result in an `OverflowError`.

Another scenario involves functions with multiple local minima. In such cases, `minimize_scalar` does not guarantee finding the global minimum.

Consider $y=x^4-x^2$, which has multiple minima. `minimize_scalar()` does not guarantee finding the global minimum. Let’s try it:

```python
from scipy.optimize import minimize_scalar
# help(minimize)

def objective_function(x):
    return x**4 - x**2

res = minimize_scalar(objective_function)
res
```
We obtain the following result:

```
 message: 
          Optimization terminated successfully;
          The returned value satisfies the termination criteria
          (using xtol = 1.48e-08 )
 success: True
     fun: -0.24999999999999994
       x: 0.7071067853059209
     nit: 11
    nfev: 14
```

The root found is 0.707. However, we know there is at least one other root at -0.707. By default, `minimize_scalar` cannot find all roots. However, we can control the solver used for optimization via parameters. There are three options:
* `brent`: Brent’s algorithm, the default for this function.
* `golden`: Golden section search. Research suggests this method performs slightly worse than `brent`.
* `bounded`: A bounded implementation of Brent’s algorithm.

`brent` and `golden` belong to the `bracket` category: a sequence of two or three elements providing an initial guess for the boundaries of the minimum region. However, these solvers **do not guarantee that the found minimum lies within this range**.

`bounded` belongs to the `bounds` category: a sequence of two elements that strictly limits the search region for the minimum. Therefore, restricting the search region is useful only when the minimum is known to lie within a specific range. We will encounter this concept further later. Let’s look at an example using bounds:

```python
# 当我们采用bounds方式限定时
res = minimize_scalar(objective_function, method='bounded', bounds=(-1, 0))
res
```

Now, the solved $x$ will fall within the interval (-1, 0), yielding:

```
 message: Solution found.
 success: True
  status: 0
     fun: -0.24999999999998732
       x: -0.707106701474177
     nit: 10
    nfev: 10
```

This time, we obtained the expected negative solution.

However, solving for an optimal asset portfolio is more complex. We must use another method, `minimize`, specifically employing the Sequential Least Squares Quadratic Programming (SLSQP) algorithm.

### Using the minimize Method

In the previous examples, we learned about objective functions, `bounds` constraints, and the `OptimizeResults` object, particularly its `fun` and `x` attributes. Next, we introduce the concept of constraints. Mastering these concepts essentially covers convex optimization.

First, let’s examine the signature of the `minimize` method:

```
scipy.optimize.minimize(fun, 
                        x0, 
                        args=(), 
                        method=None, 
                        jac=None, 
                        hess=None, 
                        hessp=None, 
                        bounds=None, 
                        constraints=(), 
                        tol=None, 
                        callback=None, 
                        options=None)
```

We will focus on parameters relevant to this chapter’s theme: `fun`, `x0`, `method`, `bounds`, and `constraints`.

`fun` refers to the objective function, which we have already encountered. If the objective function requires additional parameters, they are passed via `args`.

The optimization method uses an iterative process to find the physical quantity `x` that satisfies the objective function. It starts from a set of initial values. `x0` is the initial value provided to the optimization method. The final result is returned via `OptimalResult.x`.

Different problems require different optimization strategies. The `minimize` method supports approximately 14 optimization algorithms and allows custom algorithms. Before performing optimization, we generally need to specify an optimization algorithm.

We will introduce `bounds` and `constraints` in the context of solving for the efficient frontier, while also explaining the usage of other parameters.

First, let’s construct a minimum variance portfolio. We start by defining the objective function:

```python
def portfolio_sd(w):
    return np.sqrt(np.transpose(w) @ (returns.cov() * 253) @ w)
```

Note the constant 253. We use it to annualize returns. This is a rough but simple method. Next, we need to define constraints to achieve the requirement of "minimum volatility at a certain return rate." First, we define the annualized return:

```python
def portfolio_returns(w):
    return (np.sum(returns.mean() * w)) * 253
```

Then, we define the constraints. The `minimize` method requires constraints to be passed as a dictionary. It supports two expressions: `'eq'` (equality) and `'ineq'` (inequality).

```python
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
```

Here, we define a constraint. `'eq'` indicates that the expression pointed to by `fun` must equal zero. The value of `fun` can be a lambda expression or a regular function. This lambda expression means that the sum of weights $x$ must equal 1 (which is obvious). Note that this `fun` is not the `fun` parameter of the first argument of `minimize`; it is a constraint. Its parameters are unique, specifically the physical quantity represented by the second argument of `minimize`, `x0`.

We can also specify an `'ineq'` expression, meaning the return value of the expression or function pointed to by `fun` must be greater than zero.

```python
constraints = ({
    'type': 'ineq', 'fun': lambda x: x[0],
})
```
Similarly, here `x` is the physical quantity being solved for during iterations to satisfy the objective function. In the optimal portfolio example, it represents the weights of various assets. Therefore, `x[0]` indicates that the weight of the 0th asset must be greater than 0. This is another constraint in our example.

In reality, the constraint on asset weights is [0, 1]. The above expression only achieves half the goal. The correct approach is to use `bounds`:

```python
x0 = np.ones(len(stocks)) / len(stocks)
bounds = tuple((0,1) for _ in x0)
```
For each asset, we must establish such a bounded constraint.

Now, let’s combine all components:

```python
from scipy.optimize import minimize

res = minimize(
    fun = portfolio_sd,
    x0 = x0,
    method = 'SLSQP',
    bounds = bounds,
    constraints = constraints
)
res
```
This yields the following result:

```
 message: Optimization terminated successfully
 success: True
  status: 0
     fun: 0.14842169691096224
       x: [ 2.500e-01  2.500e-01  2.500e-01  2.500e-01]
     nit: 1
     jac: [ 0.000e+00  0.000e+00  0.000e+00  0.000e+00]
    nfev: 5
    njev: 1
```
`nit` indicates the number of function evaluations. Since we did not add a return constraint, the function essentially did nothing, as evident from the value of `x`.

Let’s try again with a return constraint:

```python
constraints = (
    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
    {'type': 'eq', 'fun': lambda x: portfolio_returns(x) - 0.1}
)

res = minimize(
    fun = portfolio_sd,
    x0 = x0,
    method = 'SLSQP',
    bounds = bounds,
    constraints = constraints,
    options = dict(disp=True)
)
res
```
!!! Info
    Note that we added an `options` parameter here. This can further reveal the iteration process.

This time, it still terminates after one iteration, but the value of weight `x` has changed. Let’s check the portfolio return calculated using these weights to see if it is 0.1:

```python
portfolio_returns(res.x)
```
The returned result is indeed 0.1, confirming the correctness of the solution process. Moreover, achieving the correct result in just one iteration is highly efficient.

Now, how should we solve for the efficient frontier?

Clearly, we should first identify the theoretical maximum and minimum returns of the portfolio, then linearly divide this interval. Each return point serves as a constraint to solve for the corresponding asset allocation weights. Based on these weights, we calculate other metrics, such as the Sharpe ratio.

The theoretical maximum return of a portfolio is obtained by allocating all positions to the best-performing stock; conversely, allocating all positions to the worst-performing asset yields the minimum return.

The `returns` table records the daily return of each instrument. We can annualize each instrument’s return using the following method:

```python
all_annual_returns = (1 + returns.mean()) ** 253 - 1
best = np.max(all_annual_returns)
worst = np.min(all_annual_returns)
print(best, worst)
```

We find that the portfolio’s maximum return is 20%, and the minimum return is -28%. Now, let’s solve for the efficient frontier, providing the complete code this time:

```python {.line-numbers}
sharpes = []
vols = []
weights = []
rets = []

all_annual_returns = (1 + returns.mean()) ** 253 - 1
best = np.max(all_annual_returns)
worst = np.min(all_annual_returns)

x0 = np.ones(len(stocks)) / len(stocks)
constraints = (
    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
    {'type': 'eq', 'fun': lambda x: portfolio_returns(x) - target}
)

# 这一次，我们要求每个标的至少分配1%的权重
bounds = tuple((0.01, 1) for _ in stocks)

for target in np.linspace(worst, best, 100):
    res = minimize(
        fun = portfolio_sd,
        x0 = x0,
        method = 'SLSQP',
        bounds = bounds,
        constraints = constraints
    )

    vols.append(res.fun)
    weights.append(res.x)
    rets.append(target)

    # 计算sharpe
    sharpe = sharpe_ratio(returns.dot(res.x))
    sharpes.append(sharpe)

# 绘制图形
plt.scatter(vols, rets, c=sharpes, cmap='RdYlBu')
pos = np.argmax(sharpes)
plt.colorbar(label='Sharpe Ratio')
plt.scatter(vols[pos], rets[pos], marker='*', s=80, color='red')

```

The total runtime was 11 seconds. It appears slower than running 5,000 Monte Carlo simulations, but it covers almost every possible combination, which 5,000 Monte Carlo simulations cannot achieve.

There are a few points in the code that require further explanation. We previously discussed the source of `x` in the lambda expression `np.sum(x) - 1`. You may have noticed that we never declared it explicitly. Actually, it is merely a formal parameter; you can use any variable name, as the `minimize` method will pass the root variable from the iteration to it—in this example, the weight matrix being solved. However, consider another constraint:

```markdown
    lambda x: portfolio_returns(x) - target
```

Where does `target` come from? How is its value passed? In fact, we must use this variable in advance, but we only declare it in the `for` loop at line 19, passing the latest value to the lambda expression.

There is also a floating-point issue. The `'eq'` expression compares its result to zero. However, due to various floating-point errors, an expression that theoretically equals zero might not be exactly zero in computer arithmetic. For example, when `portfolio_returns(x) - target < 0.001`, we might consider the optimization sufficient, but `minimize` will continue searching until the difference is less than $10^{-7}$.

We can accelerate computation by rounding the return value of `portfolio_returns` and `target` (e.g., to three decimal places). However, when doing so, we must be cautious because, without knowing the step size inside `minimize`, this could lead to optimization failure.

If further speed improvements are needed, consider using another method in the `scipy.optimize` package, `fmin_slsqp`:

```
    scipy.optimize.fmin_slsqp(
        func, 
        x0, 
        eqcons=(), 
        bounds=(), 
        acc=1e-06, 
        iprint=1, 
        disp=None, 
        full_output=0, 
        epsilon=1.4901161193847656e-08, 
        callback=None)
```
It provides `acc` and `epsilon` parameters, which align with our current approach. Their default values might also correspond to the internal defaults of `minimize`. It is also a Sequential Least Squares Quadratic Programming method. However, documentation is scarce, and there are no examples. We will not elaborate further here for your reference.

We have explored various aspects of portfolio theory and learned how to use Monte Carlo methods and convex optimization to solve for optimal asset portfolios under constraints.

However, real-world investment scenarios are more complex and cannot be fully covered by the methods introduced above. For instance, we might encounter the following situations (requirements):

1. In the mean-variance model, we include positive volatility in the calculation. However, we might only care about downside volatility—this is precisely why the Sortino ratio was invented as a strategy evaluation metric. This is just one path for optimizing our model. We might desire various new discoveries, but time and capability may not permit it.
2. So far, we have only considered positive weights, meaning we only allowed long positions. However, there is a demand for hedging risks through short selling. How should we proceed if short selling is allowed?
3. Although our universe contains 500 instruments, what if the portfolio must be limited to a maximum of 10 assets? This is not simply a matter of selecting 10 instruments and running the previous process. After all, how do we select the best 10 from a pool of 500?
4. What if we desire sector neutralization (i.e.,均衡配置 assets across sectors to avoid excessive concentration in any single industry)?
