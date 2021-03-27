#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd


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


def split_data_non_ts(df_train, df_holdout):
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


def split_data(df_train, df_holdout):
    n = len(df_holdout.index.unique())
    train_idx_end = (
        df_train.index.max() - pd.DateOffset(days=(2 * n))
    ).strftime("%Y-%m-%d")
    val_idx_end = (df_train.index.max() - pd.DateOffset(days=n)).strftime(
        "%Y-%m-%d"
    )
    # print(train_idx_end, val_idx_end, df_train.index.max())
    train_train_index = pd.date_range(df_train.index.min(), train_idx_end)
    train_val_index = pd.date_range(
        pd.Timestamp(train_idx_end) + pd.DateOffset(days=1), val_idx_end
    )
    train_date_max = df_train.index.max()
    train_test_index = pd.date_range(
        pd.Timestamp(val_idx_end) + pd.DateOffset(days=1), train_date_max
    )
    df_train_train, df_train_val, df_train_test = (
        df_train.loc[train_train_index].copy(),
        df_train.loc[train_val_index].copy(),
        df_train.loc[train_test_index].copy(),
    )
    d = {
        "indexes": [train_train_index, train_val_index, train_test_index],
        "splits": [df_train_train, df_train_val, df_train_test],
    }
    return d


class MultipleTimeSeriesValCV:
    """Yield tuples of train_idx, val_idx, test_idx triplets
    Assumes the Index contains level 'Date'
    purges overlapping outcomes"""

    def __init__(
        self,
        n_splits=3,
        test_period_length=21,
        lookahead=None,
    ):
        self.n_splits = n_splits
        self.lookahead = lookahead
        self.test_length = test_period_length

    def split(self, X, y=None, groups=None):
        unique_dates = X.index.get_level_values("Date").unique()
        days = sorted(unique_dates, reverse=True)

        split_idx = []
        for i in range(self.n_splits):
            test_end_idx = i * self.test_length
            test_start_idx = test_end_idx + self.test_length
            val_end_idx = test_start_idx + self.lookahead - 1
            val_start_idx = val_end_idx + self.test_length
            train_end_idx = val_start_idx + self.lookahead - 1
            train_start_idx = 0
            split_idx.append(
                [
                    train_start_idx,
                    train_end_idx,
                    val_start_idx,
                    val_end_idx,
                    test_start_idx,
                    test_end_idx,
                ]
            )

        dates = X.reset_index()[["Date"]]
        for (
            _,
            train_end,
            val_start,
            val_end,
            test_start,
            test_end,
        ) in split_idx:
            train_idx = dates[(dates["Date"] <= days[train_end])].index
            val_idx = dates[
                (dates["Date"] > days[val_start])
                & (dates["Date"] <= days[val_end])
            ].index
            test_idx = dates[
                (dates["Date"] > days[test_start])
                & (dates["Date"] <= days[test_end])
            ].index
            yield train_idx, val_idx, test_idx

    def get_n_splits(self, X, y, groups=None):
        return self.n_splits


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
