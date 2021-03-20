#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from category_encoders import TargetEncoder
from sklearn.base import TransformerMixin


class DFSortByDateSetDateIndex(TransformerMixin):
    def __init__(self, date_col_name):
        self.date_col_name = date_col_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        X.sort_values(self.date_col_name, inplace=True)
        X.set_index(self.date_col_name, inplace=True)
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)


class DFGetXY(TransformerMixin):
    def __init__(self, target_col_name):
        self.target_col_name = target_col_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        df_X = X[X.columns[~X.columns.isin([self.target_col_name])]]
        y_series = X[self.target_col_name]
        return [df_X, y_series]

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)


class DFFillNa(TransformerMixin):
    def __init__(self, col_name):
        self.col_name = col_name
        self.fillter = None

    def fit(self, X, y=None):
        self.fillter = X[self.col_name].median()
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        X[self.col_name] = X[self.col_name].fillna(self.fillter)
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)


class DFAddNaIndicator(TransformerMixin):
    def __init__(self, col_name):
        self.col_name = col_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        X[self.col_name + "_na"] = pd.isnull(X[self.col_name])
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)


class DFTargetEncodeCategoricalFeatures(TransformerMixin):
    def __init__(self, categoricals):
        self.categoricals = categoricals

    def fit(self, X, y=None):
        self.te = TargetEncoder(handle_missing="value")
        _ = self.te.fit(X, cols=self.categoricals, y=y)
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        X = self.te.transform(X)
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)


class DFLog1p(TransformerMixin):
    def __init__(self, col_name):
        self.col_name = col_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        X[self.col_name] = np.log1p(X[self.col_name])
        return X

    def fit_transform(self, X, y=None, **kwargs):
        self = self.fit(X, y)
        return self.transform(X)
