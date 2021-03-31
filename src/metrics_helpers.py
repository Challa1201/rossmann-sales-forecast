#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
from sklearn.metrics import mean_squared_error

# Define evaluation metric (RMSPE)
# - https://www.kaggle.com/c/rossmann-store-sales/discussion/16794


def get_weights(y):
    w = np.zeros(y.shape, dtype=float)
    ind = y != 0
    w[ind] = 1.0 / (y[ind] ** 2)
    return w


def rmspe(yhat, y):
    y = np.exp(y) - 1  # same as np.expm1(y)
    yhat = np.exp(yhat) - 1  # same as np.expm1(yhat)
    w = get_weights(y)
    rmspe = np.sqrt(np.mean(w * (y - yhat) ** 2))
    return rmspe


def rmspe_xg(yhat, y):
    y = y.get_label()
    y = np.exp(y) - 1  # same as np.expm1(y)
    yhat = np.exp(yhat) - 1  # same as np.expm1(yhat)
    w = get_weights(y)
    rmspe = np.sqrt(np.mean(w * (y - yhat) ** 2))
    return "rmspe", rmspe


def rmse(y_true, y_pred):
    # need np.expm1(...) since target was log-scaled in step 11. of
    # 4_xgboost_trials.ipynb
    rmse_score = mean_squared_error(
        np.expm1(y_true), np.expm1(y_pred), sample_weight=None, squared=False
    )
    return rmse_score
