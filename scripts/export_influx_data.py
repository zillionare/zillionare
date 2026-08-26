#!/usr/bin/env python3

from __future__ import annotations

import gzip
from io import StringIO
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import TextIO

import pandas as pd
import requests


EXPORT_COLUMNS = ["_time", "code", "amount", "close", "factor", "high", "low", "open", "volume"]
EXPORT_FIELDS = EXPORT_COLUMNS[2:]
FIELD_FILTER = " or ".join(f'r._field == "{field}"' for field in EXPORT_FIELDS)


def query_day(day: date) -> pd.DataFrame:
    start = datetime(day.year, day.month, day.day, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    stop = datetime(day.year, day.month, day.day, tzinfo=timezone.utc) + timedelta(days=1)
    stop_text = stop.isoformat().replace("+00:00", "Z")

    flux = f'''
from(bucket: "zillionare")
  |> range(start: {start}, stop: {stop_text})
  |> filter(fn: (r) => r._measurement == "stock_bars_1m")
    |> filter(fn: (r) => {FIELD_FILTER})
  |> keep(columns: ["_time", "code", "_field", "_value"])
    |> pivot(rowKey: ["_time", "code"], columnKey: ["_field"], valueColumn: "_value")
    |> keep(columns: ["_time", "code", "amount", "close", "factor", "high", "low", "open", "volume"])
    |> sort(columns: ["_time", "code"])
'''.strip()

    response = requests.post(
        "http://localhost:58086/api/v2/query?org=zillionare",
        headers={
            "Authorization": "Token influx",
            "Accept": "application/csv",
            "Content-Type": "application/vnd.flux",
        },
        data=flux.encode("utf-8"),
        timeout=600,
    )
    response.raise_for_status()

    csv_text = response.text
    if not csv_text.strip():
        return pd.DataFrame(columns=EXPORT_COLUMNS)

    data_lines = [line for line in csv_text.splitlines() if line and not line.startswith("#")]
    if len(data_lines) <= 1:
        return pd.DataFrame(columns=EXPORT_COLUMNS)

    frame = pd.read_csv(
        StringIO("\n".join(data_lines)),
        comment="#",
        usecols=lambda column: column in EXPORT_COLUMNS,
    )
    if frame.empty:
        return pd.DataFrame(columns=EXPORT_COLUMNS)

    frame = frame.reindex(columns=EXPORT_COLUMNS)
    return frame.sort_values(["_time", "code"], kind="stable")


def append_month(day: date, writer: TextIO, write_header: bool) -> bool:
    frame = query_day(day)
    if frame.empty:
        return write_header

    frame.to_csv(writer, index=False, header=not write_header)
    return True


def export_all() -> None:
    output_dir = Path.cwd() / "1m"
    output_dir.mkdir(parents=True, exist_ok=True)

    current = date(2005, 1, 1)
    stop = date(2024, 1, 1)

    while current < stop:
        month_start = current.replace(day=1)
        if month_start.month == 12:
            next_month = date(month_start.year + 1, 1, 1)
        else:
            next_month = date(month_start.year, month_start.month + 1, 1)

        output_path = output_dir / f"{month_start.year:04d}_{month_start.month:02d}.csv.gz"
        wrote_any = False

        with gzip.open(output_path, "wt", encoding="utf-8", newline="") as handle:
            day = month_start
            while day < next_month and day < stop:
                wrote_any = append_month(day, handle, wrote_any)
                day += timedelta(days=1)

        if not wrote_any:
            output_path.unlink(missing_ok=True)

        print(f"[1m] finished {month_start.year:04d}_{month_start.month:02d}")
        current = next_month


if __name__ == "__main__":
    export_all()
