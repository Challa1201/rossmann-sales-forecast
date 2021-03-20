#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd


def summarize_hyperopt_trials(trials):
    df_summary_table = (
        pd.DataFrame.from_records(
            trials.trials[k]["misc"]["vals"] for k in range(len(trials.trials))
        )
        .merge(
            pd.concat(
                [
                    pd.Series(trials.trials[k]["result"]).to_frame().T
                    for k in range(len(trials.trials))
                ]
            ).reset_index(drop=True),
            left_index=True,
            right_index=True,
        )
        .sort_values(by="loss")
    )
    return df_summary_table
