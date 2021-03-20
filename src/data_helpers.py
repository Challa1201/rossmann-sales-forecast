#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np


def left_merge_dfs(df_left, df_right, left_on, right_on=None, suffix="_y"):
    if right_on is None:
        right_on = left_on
    df_merged = df_left.merge(
        df_right,
        how="left",
        left_on=left_on,
        right_on=right_on,
        suffixes=("", suffix),
    )
    return df_merged


def split_data(df_train, df_holdout):
    n = len(df_holdout)
    idx = np.arange(0, len(df_train))
    idx.sort()
    train_idx_end = len(df_train) - (2 * n)
    val_idx_end = len(df_train) - (1 * n)
    train_train_index = idx[:train_idx_end]
    train_val_index = idx[train_idx_end:val_idx_end]
    train_test_index = idx[val_idx_end:]
    df_train_train, df_train_val, df_train_test = (
        df_train.iloc[train_train_index].copy(),
        df_train.iloc[train_val_index].copy(),
        df_train.iloc[train_test_index].copy(),
    )
    d = {
        "indexes": [train_train_index, train_val_index, train_test_index],
        "splits": [df_train_train, df_train_val, df_train_test],
    }
    return d


def sample_train_val_split(
    n_train, n_test, train_sample_size, valid_sample_size
):
    train_idx = np.random.permutation(range(n_train))[:train_sample_size]
    train_idx.sort()
    train_train_index = train_idx[:valid_sample_size]
    train_es_index = train_idx[valid_sample_size:]
    test_index_sampled = np.random.permutation(range(n_test))[
        :valid_sample_size
    ]
    return [train_train_index, train_es_index, test_index_sampled, train_idx]
