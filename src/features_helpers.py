#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re

import numpy as np
import pandas as pd


def add_datepart(df, fldname, drop=True, time=False, inplace=False):
    "Helper function that adds columns relevant to a date."
    fld = df[fldname]
    fld_dtype = fld.dtype
    if isinstance(fld_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        fld_dtype = np.datetime64

    if not np.issubdtype(fld_dtype, np.datetime64):
        df[fldname] = fld = pd.to_datetime(fld, infer_datetime_format=True)
    targ_pre = re.sub("[Dd]ate$", "", fldname)
    attr = [
        "Year",
        "Month",
        "Week",
        "Day",
        "Dayofweek",
        "Dayofyear",
        "Is_month_end",
        "Is_month_start",
        "Is_quarter_end",
        "Is_quarter_start",
        "Is_year_end",
        "Is_year_start",
    ]
    if time:
        attr = attr + ["Hour", "Minute", "Second"]
    for n in attr:
        df[targ_pre + n] = getattr(fld.dt, n.lower())
    df[targ_pre + "Elapsed"] = fld.astype(np.int64) // 10 ** 9
    if drop:
        df.drop(fldname, axis=1, inplace=True)
    if not inplace:
        return df


def get_elapsed(df, fld, pre):
    day1 = np.timedelta64(1, "D")
    last_date = np.datetime64()
    last_store = 0
    res = []

    for s, v, d in zip(df.Store.values, df[fld].values, df.Date.values):
        if s != last_store:
            last_date = np.datetime64()
            last_store = s
        if v:
            last_date = d
        res.append(((d - last_date).astype("timedelta64[D]") / day1))
    df[pre + fld] = res
