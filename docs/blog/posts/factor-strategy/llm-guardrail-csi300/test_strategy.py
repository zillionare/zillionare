import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from strategy import Config, backtest, make_features, normalise


def sample_prices(days=1400):
    index = pd.bdate_range("2018-01-01", periods=days)
    close = 100 * np.cumprod(1 + 0.0002 + 0.01 * np.sin(np.arange(days) / 13))
    return pd.DataFrame({"close": close}, index=index)


def test_long_only_and_outputs(tmp_path):
    result, metrics, notes = backtest(make_features(sample_prices()), Config(), "rule", tmp_path)
    assert not result.empty
    assert result.position.between(0, 1).all()
    assert result.equity.notna().all()
    assert metrics["observations"] == len(result) - 1
    assert notes


def test_chinese_csv_fields_are_accepted():
    raw = sample_prices(900).reset_index().rename(columns={"index": "日期", "close": "收盘"})
    output = normalise(raw, "日期", "收盘")
    assert len(output) == 900
