#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd


def get_xgboost_training_curves(training_curves, metric="rmspe"):
    df_training_curves = pd.DataFrame(
        training_curves["train"][metric], columns=["train"]
    ).merge(
        pd.DataFrame(training_curves["eval"][metric], columns=["eval"]),
        left_index=True,
        right_index=True,
    )
    return df_training_curves
