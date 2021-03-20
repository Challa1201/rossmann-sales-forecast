#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd


def get_xgboost_preds_obs(y_true, y_pred):
    left = pd.DataFrame(
        y_pred, columns=["pred"], index=y_true.index
    ).reset_index()
    right = y_true.reset_index()
    df_pred = left.merge(right, left_index=True, right_index=True, how="inner")
    return df_pred
