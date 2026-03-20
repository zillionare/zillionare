#!/usr/bin/env python3
"""
UBL因子月度调仓回测框架 - 使用empyrical-reloaded进行策略评估
基于东吴证券研报《上下影线，蜡烛好还是威廉好？》
实现月度调仓策略并使用empyrical计算标准化评估指标
"""

import datetime
import os
import sys
import warnings
from typing import Dict, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 导入empyrical-reloaded
try:
    import empyrical
except ImportError:
    print("请安装empyrical-reloaded: pip install empyrical-reloaded")
    sys.exit(1)

warnings.filterwarnings("ignore")

# 添加startup.py路径
sys.path.insert(0, os.path.expanduser("./scripts"))
from data import *

# 导入UBL因子计算函数
from ubl_factor_analysis import (
    calculate_lower_shadow,
    calculate_ubl_factor,
    calculate_upper_shadow,
    calculate_williams_r_down,
    calculate_williams_r_up,
    prepare_factor_data,
)


def run_monthly_rebalance_test(
    factor_data: pd.Series,
    prices: pd.DataFrame,
    n_groups: int = 5,
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None,
    benchmark_col: Optional[str] = None,
) -> Tuple[Dict, Dict]:
    """
    实现月度调仓回测框架

    Args:
        factor_data: 因子数据 (MultiIndex: date, asset)
        prices: 价格数据 (Index: date, Columns: asset)
        n_groups: 分组数量
        start_date: 回测开始日期，默认为None表示使用全部数据
        end_date: 回测结束日期，默认为None表示使用全部数据
        benchmark_col: 基准列名，如果提供则计算相对基准的指标

    Returns:
        group_returns: 每组每月收益率序列
        performance: 每组的评估指标
    """
    # 确保日期索引格式正确
    factor_data = factor_data.copy()
    if not isinstance(factor_data.index, pd.MultiIndex):
        raise ValueError("factor_data must have MultiIndex with (date, asset)")

    # 转换日期格式
    dates = pd.to_datetime(factor_data.index.get_level_values("date").unique())
    prices.index = pd.to_datetime(prices.index)

    # 应用日期过滤
    if start_date:
        start_date = pd.to_datetime(start_date)
        dates = dates[dates >= start_date]
        prices = prices.loc[prices.index >= start_date]

    if end_date:
        end_date = pd.to_datetime(end_date)
        dates = dates[dates <= end_date]
        prices = prices.loc[prices.index <= end_date]

    # 获取月末日期列表
    month_ends = []
    for date in sorted(dates):
        # 检查是否是当月的最后一个交易日
        next_day = date + pd.Timedelta(days=1)
        while next_day.month == date.month:
            if next_day in dates:
                break
            next_day += pd.Timedelta(days=1)

        if next_day.month != date.month or next_day not in dates:
            month_ends.append(date)

    month_ends = pd.DatetimeIndex(month_ends)

    print(f"Testing period: {month_ends[0]} to {month_ends[-1]}")
    print(
        f"Total months: {len(month_ends) - 1}"
    )  # 减1因为最后一个月末没有下一个月的收益率

    # 存储每组每月收益率
    group_monthly_returns = {}

    # 对每个月末进行回测
    for i in range(len(month_ends) - 1):
        # 当前月末和下一个月末
        current_month_end = month_ends[i]
        next_month_end = month_ends[i + 1]

        # 获取当前月末的因子值
        try:
            month_end_factors = factor_data.xs(current_month_end, level="date")

            # 过滤掉NaN值
            month_end_factors = month_end_factors.dropna()

            if len(month_end_factors) < n_groups:
                print(
                    f"Warning: Not enough stocks with valid factor values on {current_month_end}"
                )
                continue

            # 按因子值分组
            factor_quantiles = pd.qcut(month_end_factors, n_groups, labels=False) + 1

            # 确保价格数据中有当前月末和下一个月末
            if (
                current_month_end not in prices.index
                or next_month_end not in prices.index
            ):
                print(
                    f"Warning: Missing price data for {current_month_end} or {next_month_end}"
                )
                continue

            # 获取下个月的收益率
            next_month_returns = (
                prices.loc[next_month_end] / prices.loc[current_month_end] - 1
            )

            # 计算每组的等权收益率
            for group in range(1, n_groups + 1):
                group_assets = factor_quantiles[factor_quantiles == group].index

                # 过滤掉价格数据中没有的资产
                valid_assets = [
                    asset for asset in group_assets if asset in next_month_returns.index
                ]

                if len(valid_assets) > 0:
                    group_return = next_month_returns[valid_assets].mean()

                    if group not in group_monthly_returns:
                        group_monthly_returns[group] = []

                    group_monthly_returns[group].append(
                        {
                            "date": next_month_end,
                            "return": group_return,
                            "n_stocks": len(valid_assets),
                        }
                    )
        except Exception as e:
            print(f"Error processing month end {current_month_end}: {e}")
            continue

    # 转换为DataFrame
    group_returns = {}
    performance = {}

    # 获取基准收益率
    benchmark_returns = None
    if benchmark_col and benchmark_col in prices.columns:
        benchmark_prices = prices[benchmark_col]
        benchmark_returns = benchmark_prices.pct_change().dropna()

    for group, returns in group_monthly_returns.items():
        if not returns:
            print(f"Warning: No returns data for group {group}")
            continue

        returns_df = pd.DataFrame(returns)
        returns_df.set_index("date", inplace=True)
        group_returns[group] = returns_df

        # 提取月度收益率序列
        monthly_returns = returns_df["return"]

        # 使用empyrical计算评估指标
        performance[group] = calculate_performance_metrics(
            monthly_returns, benchmark=benchmark_returns if benchmark_col else None
        )

        # 添加平均持仓数量
        performance[group]["avg_stocks_per_month"] = returns_df["n_stocks"].mean()

    # 计算多空组合
    if 1 in group_returns and n_groups in group_returns:
        # 确保两个组的日期索引一致
        common_dates = group_returns[1].index.intersection(
            group_returns[n_groups].index
        )

        if len(common_dates) > 0:
            long_short_returns = (
                group_returns[n_groups].loc[common_dates, "return"]
                - group_returns[1].loc[common_dates, "return"]
            )

            # 使用empyrical计算多空组合的评估指标
            performance["long_short"] = calculate_performance_metrics(
                long_short_returns,
                benchmark=benchmark_returns if benchmark_col else None,
            )

            # 添加多空组合到group_returns
            long_short_df = pd.DataFrame(
                {
                    "return": long_short_returns,
                    "n_stocks": 0,  # 多空组合没有实际持仓数量
                }
            )
            group_returns["long_short"] = long_short_df

    # 打印性能指标
    print("\n分组回测结果:")
    metrics_to_display = [
        "annual_return",
        "annual_volatility",
        "sharpe_ratio",
        "sortino_ratio",
        "max_drawdown",
        "calmar_ratio",
        "win_rate",
    ]

    for group in sorted(
        performance.keys(), key=lambda x: x if isinstance(x, int) else float("inf")
    ):
        metrics = performance[group]
        print(f"\n组别 {group}:")
        for metric in metrics_to_display:
            if metric in metrics:
                value = metrics[metric]
                if isinstance(value, float):
                    print(f"  {metric}: {value:.4f}")
                else:
                    print(f"  {metric}: {value}")

        if "avg_stocks_per_month" in metrics:
            print(f"  avg_stocks_per_month: {metrics['avg_stocks_per_month']:.1f}")

    return group_returns, performance


def calculate_performance_metrics(returns, benchmark=None, risk_free=0.0):
    """使用empyrical计算策略评估指标"""
    metrics = {}

    # 年化收益率
    metrics["annual_return"] = empyrical.annual_return(returns)

    # 年化波动率
    metrics["annual_volatility"] = empyrical.annual_volatility(returns)

    # 夏普比率
    metrics["sharpe_ratio"] = empyrical.sharpe_ratio(returns, risk_free=risk_free)

    # 索提诺比率
    metrics["sortino_ratio"] = empyrical.sortino_ratio(
        returns, required_return=risk_free
    )

    # 最大回撤
    metrics["max_drawdown"] = empyrical.max_drawdown(returns)

    # 卡玛比率
    metrics["calmar_ratio"] = empyrical.calmar_ratio(returns)

    # 胜率
    metrics["win_rate"] = (returns > 0).mean()

    # 总收益率
    metrics["total_return"] = (1 + returns).prod() - 1

    # 如果提供了基准，计算相对基准的指标
    if benchmark is not None:
        # 确保日期对齐
        aligned_returns, aligned_benchmark = returns.align(benchmark, join="inner")

        if len(aligned_returns) > 0:
            # Alpha
            metrics["alpha"] = empyrical.alpha(
                aligned_returns, aligned_benchmark, risk_free=risk_free
            )

            # Beta
            metrics["beta"] = empyrical.beta(aligned_returns, aligned_benchmark)

            # 信息比率
            metrics["information_ratio"] = empyrical.excess_sharpe(
                aligned_returns, aligned_benchmark
            )

    return metrics


def plot_strategy_returns(
    group_returns, benchmark=None, title="UBL Factor - Monthly Rebalance Returns"
):
    """绘制策略收益率曲线（与基准对比）"""
    if not group_returns:
        print("No returns data to plot")
        return

    # 计算累积收益率
    cumulative_returns = {}
    for group, returns in group_returns.items():
        if "return" in returns.columns:
            cumulative_returns[group] = (1 + returns["return"]).cumprod() - 1

    # 绘制累积收益率
    plt.figure(figsize=(12, 8))

    # 如果有基准，先绘制基准
    if benchmark is not None:
        benchmark_cum = (1 + benchmark).cumprod() - 1
        plt.plot(
            benchmark_cum.index, benchmark_cum, "k-", linewidth=1.5, label="Benchmark"
        )

    # 绘制分组收益率
    colors = plt.cm.viridis(
        np.linspace(
            0, 0.8, len([g for g in cumulative_returns.keys() if g != "long_short"])
        )
    )
    color_idx = 0

    for group in sorted([g for g in cumulative_returns.keys() if g != "long_short"]):
        plt.plot(
            cumulative_returns[group].index,
            cumulative_returns[group],
            color=colors[color_idx],
            linewidth=1.5,
            label=f"Group {group}",
        )
        color_idx += 1

    # 最后绘制多空组合，使其更突出
    if "long_short" in cumulative_returns:
        plt.plot(
            cumulative_returns["long_short"].index,
            cumulative_returns["long_short"],
            "r--",
            linewidth=2,
            label="Long-Short (5-1)",
        )

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # 添加收益率标签
    for group, cum_ret in cumulative_returns.items():
        if not cum_ret.empty:
            final_return = cum_ret.iloc[-1]
            plt.annotate(
                f"{final_return:.2%}",
                xy=(cum_ret.index[-1], final_return),
                xytext=(5, 0),
                textcoords="offset points",
                fontsize=9,
            )

    return plt


def create_equal_weight_benchmark(prices):
    """创建等权基准组合"""
    # 计算每日收益率
    daily_returns = prices.pct_change().dropna()

    # 计算等权组合收益率
    equal_weight_returns = daily_returns.mean(axis=1)

    return equal_weight_returns


def main():
    """主函数"""
    # 设置参数
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    universe_size = 100  # 股票池大小
    n_groups = 5  # 分组数量

    try:
        print(f"=== UBL因子月度调仓回测 ({start_date} to {end_date}) ===")
        print(f"股票池大小: {universe_size}")
        print(f"分组数量: {n_groups}")

        # 准备数据
        factor_data, prices = prepare_factor_data(start_date, end_date, universe_size)

        # 创建等权基准
        print("创建等权基准组合...")
        benchmark_returns = create_equal_weight_benchmark(prices)

        # 将基准收益率转换为月度收益率
        monthly_benchmark = []

        # 获取月末日期
        dates = pd.to_datetime(factor_data.index.get_level_values("date").unique())
        month_ends = []
        for date in sorted(dates):
            next_day = date + pd.Timedelta(days=1)
            while next_day.month == date.month:
                if next_day in dates:
                    break
                next_day += pd.Timedelta(days=1)

            if next_day.month != date.month or next_day not in dates:
                month_ends.append(date)

        month_ends = pd.DatetimeIndex(month_ends)

        # 计算月度基准收益率
        for i in range(len(month_ends) - 1):
            current_month_end = month_ends[i]
            next_month_end = month_ends[i + 1]

            if (
                current_month_end in benchmark_returns.index
                and next_month_end in benchmark_returns.index
            ):
                # 计算月度收益率
                monthly_return = (
                    1 + benchmark_returns.loc[current_month_end:next_month_end]
                ).prod() - 1
                monthly_benchmark.append(
                    {"date": next_month_end, "return": monthly_return}
                )

        monthly_benchmark_df = pd.DataFrame(monthly_benchmark)
        if not monthly_benchmark_df.empty:
            monthly_benchmark_df.set_index("date", inplace=True)
            benchmark_monthly_returns = monthly_benchmark_df["return"]
        else:
            benchmark_monthly_returns = None
            print("Warning: Failed to create monthly benchmark returns")

        # 运行月度调仓回测
        print("\n执行月度调仓回测...")
        group_returns, performance = run_monthly_rebalance_test(
            factor_data,
            prices,
            n_groups=n_groups,
            start_date=start_date,
            end_date=end_date,
        )

        if group_returns:
            # 绘制收益率图表
            plt = plot_strategy_returns(
                group_returns,
                benchmark=benchmark_monthly_returns,
                title=f"UBL Factor - Monthly Rebalance ({start_date} to {end_date})",
            )
            plt.savefig("ubl_monthly_returns.png", dpi=150, bbox_inches="tight")
            plt.show()

            # 保存结果到CSV
            results_df = pd.DataFrame()
            for group, metrics in performance.items():
                group_name = (
                    f"Group {group}" if group != "long_short" else "Long-Short (5-1)"
                )
                results_df[group_name] = pd.Series(metrics)

            results_df.to_csv("ubl_monthly_performance.csv")
            print(f"\n结果已保存到 'ubl_monthly_performance.csv'")

            # 保存月度收益率
            monthly_returns_df = pd.DataFrame()
            for group, returns in group_returns.items():
                group_name = (
                    f"Group {group}" if group != "long_short" else "Long-Short (5-1)"
                )
                monthly_returns_df[group_name] = returns["return"]

            # 添加基准收益率
            if benchmark_monthly_returns is not None:
                # 确保日期对齐
                aligned_benchmark = benchmark_monthly_returns.reindex(
                    monthly_returns_df.index
                )
                monthly_returns_df["Benchmark"] = aligned_benchmark

            monthly_returns_df.to_csv("ubl_monthly_returns_data.csv")
            print(f"月度收益率数据已保存到 'ubl_monthly_returns_data.csv'")

            # 使用quantstats生成报告（如果安装了）
            try:
                import quantstats as qs

                # 为最佳组合生成报告
                best_group = max(
                    [g for g in performance.keys() if g != "long_short"],
                    key=lambda g: performance[g]["sharpe_ratio"],
                )
                best_returns = group_returns[best_group]["return"]

                # 生成HTML报告
                qs.reports.html(
                    best_returns,
                    benchmark=(
                        benchmark_monthly_returns
                        if benchmark_monthly_returns is not None
                        else None
                    ),
                    title=f"UBL Factor - Group {best_group}",
                    output=f"ubl_group{best_group}_report.html",
                )
                print(
                    f"\n已生成Group {best_group}的quantstats报告: ubl_group{best_group}_report.html"
                )

                # 为多空组合生成报告
                if "long_short" in group_returns:
                    ls_returns = group_returns["long_short"]["return"]
                    qs.reports.html(
                        ls_returns,
                        benchmark=(
                            benchmark_monthly_returns
                            if benchmark_monthly_returns is not None
                            else None
                        ),
                        title="UBL Factor - Long-Short Portfolio",
                        output="ubl_longshort_report.html",
                    )
                    print("已生成多空组合的quantstats报告: ubl_longshort_report.html")

            except ImportError:
                print("\n提示: 安装quantstats-reloaded可以生成更详细的策略报告")
                print("pip install quantstats-reloaded")

            print("\nUBL因子月度调仓回测完成!")
        else:
            print("回测失败，未能生成有效的收益率数据。")

    except Exception as e:
        print(f"Error in main execution: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
