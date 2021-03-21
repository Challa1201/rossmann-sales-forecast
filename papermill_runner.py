#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import shlex
import subprocess
from datetime import datetime
from typing import Dict, List

import papermill as pm

PROJ_ROOT_DIR = os.path.abspath(os.getcwd())
data_dir = os.path.join(PROJ_ROOT_DIR, "data")
output_notebook_dir = os.path.join(PROJ_ROOT_DIR, "executed_notebooks")

raw_data_path = os.path.join(data_dir, "raw")

zero_dict_nb_name = "0_get_data.ipynb"
one_dict_nb_name = "1_data_clean_feat_eng.ipynb"
four_dict_nb_name = "4_xgboost_trials.ipynb"

zero_dict = dict(
    base_url=str(os.getenv("BASE_URL")), tar_filename_no_extension="rossmann"
)
one_dict = dict(
    dataset_names=[
        "store",
        "state_names",
        "store_states",
        "test",
        "train",
        "weather",
    ],
    train_date_max="2015-07-25",
)
four_dict = dict(
    columns=[
        "Store",
        "DayOfWeek",
        "Year",
        "Month",
        "Day",
        "StateHoliday",
        "CompetitionMonthsOpen",
        "Promo2Weeks",
        "StoreType",
        "Assortment",
        "PromoInterval",
        "CompetitionOpenSinceYear",
        "Promo2SinceYear",
        "State",
        "Week",
        "Events",
        "Promo_fw",
        "Promo_bw",
        "StateHoliday_fw",
        "StateHoliday_bw",
        "SchoolHoliday_fw",
        "SchoolHoliday_bw",
        "CompetitionDistance",
        "Max_TemperatureC",
        "Mean_TemperatureC",
        "Min_TemperatureC",
        "Max_Humidity",
        "Mean_Humidity",
        "Min_Humidity",
        "Max_Wind_SpeedKm_h",
        "Mean_Wind_SpeedKm_h",
        "CloudCover",
        "AfterStateHoliday",
        "BeforeStateHoliday",
        "Promo",
        "SchoolHoliday",
        "Date",
        "Sales",
    ],
    continuous_vars_missing_vals=["CompetitionDistance", "CloudCover"],
)


def run_cmd(cmd: str) -> None:
    print(cmd)
    process = subprocess.Popen(
        shlex.split(cmd), shell=False, stdout=subprocess.PIPE
    )
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print(str(output.strip(), "utf-8"))
    _ = process.poll()


def papermill_run_notebook(
    nb_dict: Dict, output_notebook_dir: str = "executed_notebooks"
) -> None:
    """Execute notebook with papermill"""
    for notebook, nb_params in nb_dict.items():
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_nb = os.path.basename(notebook).replace(
            ".ipynb", f"-{now}.ipynb"
        )
        print(
            f"\nInput notebook path: {notebook}",
            f"Output notebook path: {output_notebook_dir}/{output_nb} ",
            sep="\n",
        )
        for key, val in nb_params.items():
            print(key, val, sep=": ")
        pm.execute_notebook(
            input_path=notebook,
            output_path=f"{output_notebook_dir}/{output_nb}",
            parameters=nb_params,
        )


def run_notebooks(
    notebook_list: List, output_notebook_dir: str = "executed_notebooks"
) -> None:
    """Execute notebooks from CLI.
    Parameters
    ----------
    nb_dict : List
        list of notebooks to be executed
    Usage
    -----
    > import os
    > PROJ_ROOT_DIR = os.path.abspath(os.getcwd())
    > one_dict_nb_name = "a.ipynb
    > one_dict = {"a": 1}
    > run_notebook(
          notebook_list=[
              {os.path.join(PROJ_ROOT_DIR, one_dict_nb_name): one_dict}
          ]
      )
    """
    for nb in notebook_list:
        papermill_run_notebook(
            nb_dict=nb, output_notebook_dir=output_notebook_dir
        )


if __name__ == "__main__":
    PROJ_ROOT_DIR = os.getcwd()
    nb_dict_list = [
        zero_dict,
        one_dict,
        # four_dict,
    ]
    nb_name_list = [zero_dict_nb_name, one_dict_nb_name, four_dict_nb_name]
    notebook_list = [
        {os.path.join(PROJ_ROOT_DIR, nb_name): nb_dict}
        for nb_dict, nb_name in zip(nb_dict_list, nb_name_list)
    ]
    run_notebooks(
        notebook_list=notebook_list, output_notebook_dir=output_notebook_dir
    )
