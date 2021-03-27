#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd


def test_train_test_target_var(df_train, df_test, y_var_name):
    assert y_var_name not in list(df_test)
    assert df_test.shape[1] + 1 == df_train.shape[1]


def test_dfgetxy(X, y, y_name):
    assert y_name not in list(X)
    assert y.name == "Sales"


def test_split_data_non_ts(
    train_idx_end,
    val_idx_end,
    test_idx_end,
    df_val,
    df_test,
    df_holdout,
):
    """
    Usage
    -----
    d = split_data(df_train_full, df_holdout)
    train_index, val_index, test_index = d["indexes"]
    df_train, df_val, df_test = d["splits"]
    test_split_data_non_ts(
        max(train_index),
        max(val_index),
        max(test_index),
        df_val,
        df_test,
        df_holdout,
    )
    """
    # Check length of validation split
    assert val_idx_end - train_idx_end == len(df_holdout)
    # Check length of testing split
    assert test_idx_end - val_idx_end == len(df_holdout)
    assert len(df_val) == len(df_test)


def test_split_data(
    train_train_index,
    train_val_index,
    train_test_index,
    n_holdout,
):
    assert len(train_val_index) == len(train_test_index) == n_holdout
    # Check boundary between validation and testing splits
    assert train_test_index.min().strftime("%Y-%m-%d") == (
        train_val_index.max() + pd.DateOffset(days=1)
    ).strftime("%Y-%m-%d")
    # Check boundary between training and validation splits
    assert train_val_index.min().strftime("%Y-%m-%d") == (
        train_train_index.max() + pd.DateOffset(days=1)
    ).strftime("%Y-%m-%d")


def test_fillna(X_train, X_val, X_test, continuous_vars_missing_vals):
    assert (X_train[continuous_vars_missing_vals].isna().sum().tolist()) == [
        0
    ] * len(continuous_vars_missing_vals)
    assert (X_val[continuous_vars_missing_vals].isna().sum().tolist()) == [
        0
    ] * len(continuous_vars_missing_vals)
    assert (X_test[continuous_vars_missing_vals].isna().sum().tolist()) == [
        0
    ] * len(continuous_vars_missing_vals)
    for c in continuous_vars_missing_vals:
        assert c + "_na" in list(X_train)
        assert c + "_na" in list(X_val)
        assert c + "_na" in list(X_test)


def test_target_encode_categorical_features(X_train, X_val, X_test):
    assert not list(X_train.select_dtypes(include="object"))
    assert not list(X_val.select_dtypes(include="object"))
    assert not list(X_test.select_dtypes(include="object"))


def test_sampled_data_sizes(
    train_index,
    val_index,
    test_index,
    val_sample_size,
    index,
    df_train,
    df_val,
    df_test,
):
    assert np.array_equal(np.concatenate((train_index, val_index)), index)
    assert len(test_index) == val_sample_size
    assert len(df_train) == val_sample_size
    assert len(df_val) == len(df_test) == val_sample_size


def test_log1p(s_s):
    for s in s_s:
        assert s.min() >= 1
