#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from sklearn.base import TransformerMixin

import src.features_helpers as fh


class DFOneWayDateFilter(TransformerMixin):
    def __init__(
        self, date_col_name, date_boundary_inclusive, comp_operator="le"
    ):
        self.date_col_name = date_col_name
        self.date_boundary_inclusive = date_boundary_inclusive
        self.comp_operator = comp_operator

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        date_col_datetime = pd.to_datetime(X[self.date_col_name])
        if self.comp_operator == "le":
            date_mask = date_col_datetime <= self.date_boundary_inclusive
        elif self.comp_operator == "ge":
            date_mask = date_col_datetime >= self.date_boundary_inclusive
        else:
            date_mask = date_col_datetime == self.date_boundary_inclusive
        X = X.loc[date_mask].reset_index(drop=True)
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)


class DFStr2Bool(TransformerMixin):
    def __init__(self, col_name, str2replace, comparison="ne"):
        self.col_name = col_name
        self.str2replace = str2replace
        self.comparison = comparison

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        if self.comparison == "ne":
            X[self.col_name] = X[self.col_name] != self.str2replace
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)


class DFAddDatePart(TransformerMixin):
    def __init__(
        self,
        date_col_name="Date",
        drop=False,
        time=False,
        inplace=False,
    ):
        self.date_col_name = date_col_name
        self.drop = drop
        self.time = time
        self.inplace = inplace

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        X = fh.add_datepart(
            X,
            self.date_col_name,
            drop=self.drop,
            time=self.time,
            inplace=self.inplace,
        )
        return X


class DFDropColsBySuffix(TransformerMixin):
    def __init__(self, suffix):
        self.suffix = suffix

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        for c in X.columns:
            if c.endswith(self.suffix):
                if c in X.columns:
                    X.drop(c, inplace=True, axis=1)
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)


class DFFillNaPlaceHolder(TransformerMixin):
    def __init__(self, col_name, placeholder):
        self.col_name = col_name
        self.placeholder = placeholder

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        X[self.col_name] = X[self.col_name].fillna(self.placeholder)
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)


class DFDtypeChanger(TransformerMixin):
    def __init__(self, col_name, dtype):
        self.col_name = col_name
        self.dtype = dtype

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        X[self.col_name] = X[self.col_name].astype(self.dtype)
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)


class DFToDatetime(TransformerMixin):
    def __init__(self, col_name):
        self.col_name = col_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        X[self.col_name] = pd.to_datetime(X[self.col_name])
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)


class DFMultiDirMultiColRollingStat(TransformerMixin):
    def __init__(self, groupby_col, cols):
        self.cols = cols
        self.groupby_col = groupby_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        bwd_looking_roll_stat = (
            X[[self.groupby_col] + self.cols]
            .sort_index()
            .groupby(self.groupby_col)[self.cols]
            .rolling(7, min_periods=1)
            .sum()
            .reset_index()
        )
        fwd_looking_roll_stat = (
            X[[self.groupby_col] + self.cols]
            .sort_index(ascending=False)
            .groupby(self.groupby_col)[self.cols]
            .rolling(7, min_periods=1)
            .sum()
            .reset_index()
        )
        X = (
            X.reset_index()
            .merge(
                bwd_looking_roll_stat,
                how="left",
                on=["Date", self.groupby_col],
                suffixes=["", "_bw"],
            )
            .merge(
                fwd_looking_roll_stat,
                how="left",
                on=["Date", self.groupby_col],
                suffixes=["", "_fw"],
            )
        )
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)
