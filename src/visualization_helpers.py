#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm


def plot_qq(
    res: pd.Series,
    fig_size: tuple = (15, 12),
) -> None:
    """Plot Q-Q (quantile-quantile) plot"""
    fig, ax = plt.subplots(figsize=fig_size)
    sm.ProbPlot(data=res, dist=stats.distributions.norm, fit=True).qqplot(
        line="s", ax=ax
    )
    ax.get_lines()[0].set_markersize(10)
    ax.grid(color="lightgrey")
    ax.set_title("Normal Q-Q plot", fontsize=16, loc="left", fontweight="bold")
