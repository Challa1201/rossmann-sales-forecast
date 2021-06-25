# [Rossmann Store sales](#rossmann-store-sales)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/edesz/rossmann-sales-forecast)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edesz/rossmann-sales-forecast/master/0_get_data.ipynb)
![CI](https://github.com/edesz/rossmann-sales-forecast/workflows/CI/badge.svg)
![CodeQL](https://github.com/edesz/rossmann-sales-forecast/workflows/CodeQL/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/mit)
![OpenSource](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![prs-welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)
![pyup](https://pyup.io/repos/github/edesz/rossmann-sales-forecast/shield.svg)

## [Table of Contents](#table-of-contents)
1. [About](#about)
   * [General Sales Forecasting](#general-sales-forecasting)
   * [Current Use-Case](#current-use-case)
   * [Practical Considerations](#practical-considerations)
   * [Objective](#objective)
2. [Limitations](#limitations)
3. [Project Organization](#project-organization)

## [About](#about)
Forecast six-weeks ahead store-wise sales for [Rossmann drug store chain in Germany](https://en.wikipedia.org/wiki/Rossmann_(company)).

### [General Sales Forecasting](#general-sales-forecasting)
Sales planning is important for companies in a high growth mode or those that are in the process of adding new products or entering into new markets.

For Rossmann, a sales forecast can have tremendous value across the entire chain of drug stores. Storewide forecasts could play an important role in operational efficiency of each individual store. Store managers, citywide/statewide/regional managers and strategic planners can use a sales forecast to design and implement sales and operational policies that maximize storewide sales revenue.

### [Current Use-Case](#current-use-case)
In the retail shopping industry, the problem of overstaffing can be a significant contributor to increased costs while understaffing can negatively impact customer satisfaction. In an attempt to help deal with these issues, as part of a strategic planning initiative designed to assist store managers with staffing arrangements, the company is looking to forecast daily store sales for a six week (1.5 months) ahead period corresponding to Aug 1, 2015 to September 17, 2015 at approximately 1,100 of the approximately 2,000 ([1](http://www.cosmetic-business.com/de/News/rossmann-continues-to-grow/381871), [2](https://www.statista.com/statistics/717960/rossmann-stores-germany/)) Rossmann stores in Germany.

Such a forecast facilitates the following
-   better staffing schedule planning in order to match number of employees servicing a single store with expected sales in that store
-   create effective staff schedules that increase productivity and motivation
-   optimal balance between the customer satisfaction and wage expense

and will help store managers stay focused on their customers and their teams.

Due to the frequency of changes in sales data, a forecast designed using historical data upto the end of 2014 might not be valid deep into 2015. So, Rossmann has picked a forecast period that is not long enough to span several months of but is also sufficiently long that store managers will consult the forecast to create meaningful staffing rotas which will more accurately meet expected customer demand than rules-based or naive forecasting techniques during this period of the year.

In-store sales are affected by numerous factors, including store location, competitors, seasonality, in-store promotions and school/state holidays. For example, this period of the year is unique in that it covers the latter half of the current academic year's school holidays in Germany and the start of the following year's school year. However, the exact dates of school holidays vary by state in Germany ([1](https://study.studentnews.eu/s/3693/75527-School-year-in-Europe/4084760-Germany-201516.htm)) and will affect store-staffing schedules differently depending on the state in which that store is located. Up to five public holidays also cover this period, depending on the state ([1](https://www.timeanddate.com/holidays/germany/2015)). Student employment at stores naturally rises during the school vacation and drops off when the school semester resumes - this impacts store managers staffing schedules during this period, and a reliable forecast will aid in creating schedules that reflect sales generated without negatively impacting customer satisfaction.

### [Practical Considerations](#practical-considerations)
The requirement of the forecast is that it be available to store managers on the first day of this period (i.e. on August 1, 2015) so that they can use it to plan store staffing operations (hiring and scheduling) over the following six weeks starting from that date (Aug 1, 2015).

Data to be used to generate a forecast ends on July 31, 2015. The sales forecast must be deployed (not shown here) before the start of business hours on Aug 1, 2015 and sales data upto the end of the business day ending on July 31, 2015 will be available soon after the end of the business hours on July 31, 2015.

The final version of the forecast can use this day's data (July 31, 2015) but it must be noted that the forecast needs to be deployed before the start of business hours on Aug 1, 2015. This is the case in order to allow store managers to review the forecast before opening for business on the morning of Aug 1, 2015.

### [Objective](#objective)
Forecast store-wise sales for approximately 1,100 of the German-based stores in the Rossmann chain over the period of Aug 1, 2015 to Sep 17, 2015, with an overall (across all stores combined) [Root Mean Squared Percentage Error](https://link.springer.com/article/10.1007/s10342-014-0793-7) (RMSPE) of 10% or less.

## [Limitations](#limitations)
1. A major technical limitation of the analysis performed here is that neither trend nor seasonality have been removed from the timeseries for each store from the data. Tree-based methods cannot extrapolate and so can't handle trend ([1](http://freerangestats.info/blog/2016/12/10/extrapolation), [2](https://srome.github.io/Dealing-With-Trends-Combine-a-Random-Walk-with-a-Tree-Based-Model-to-Predict-Time-Series-Data/)). The timeseries should have been transformed to remove the underlying signal before attempting to use ML-based techniques for timeseries forecasting. While [Deep Learning (DL)](https://en.wikipedia.org/wiki/Deep_learning) doesn't have this limitation (and was not used here), DL approaches such as [LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory) perform better at forecasting if the underlying structure has been removed from the time-series ([1](https://www.quora.com/Why-are-the-data-used-in-LSTM-needed-to-be-transformed-into-stationary-when-processing-time-series-It-seems-like-the-process-of-backpropagation-is-curve-fitting/answer/Marco-Santanch%C3%A9), [2](https://www.quora.com/Can-an-LSTM-predict-the-time-series-if-they-are-not-stationary/answer/Nowan-Ilfideme)). Again, [structure should be removed](https://www.linkedin.com/pulse/how-use-machine-learning-time-series-forecasting-vegard-flovik-phd-1f) before trying to use deep learning for forecasting.
2. A related technical complication with using ML for non-stationary timeseries forecasting is that the stationarity transformations need to be reverted to the original scale, **without using the original data**. If a ML model is developed using a training split (which has been transformed) of the overall dataset, and used to forecast an out-of-sample (test) split, then the forecast will be on the transformed scale and it needs to be inverted **without using the true values of the test split** ([1](https://machinelearningmastery.com/machine-learning-data-transforms-for-time-series-forecasting/#comment-486543)). The framework developed in this project does not make an allocation for implementing such invertibility. The above-mentioned [tutorial](https://srome.github.io/Dealing-With-Trends-Combine-a-Random-Walk-with-a-Tree-Based-Model-to-Predict-Time-Series-Data/) shows how to invert a transformation when the test set data is used to perform the inversion.  However, when generating a forecast in a real-life scenario, the test set (i.e. the real values for the period covered by the forecast) are not known. For example, when forecasting 14 days into the future, the true values of those 14 days will not be available to us and we will have to wait for 14 days in order to evaluate the forecast. If that is the case, we **also will have to wait for 14 days to have access to the true values** in order to use them to invert the forecasted values - obviously, this is not practical since we need the forecasted values (on the correct scale) as soon as they are available. For this reason, we need to pick transformations that can be reverted without using the test set (true values) - this means we must use the training data to revert the forecasted values back to the original scale.

## [Project Organization](#project-organization)

    ├── LICENSE
    ├── .env                          <- environment variables (verify this is in .gitignore)
    ├── .gitignore                    <- files and folders to be ignored by version control system
    ├── .pre-commit-config.yaml       <- configuration file for pre-commit hooks
    ├── .github
    │   ├── workflows
    │       └── integrate.yml         <- configuration file for CI build on Github Actions
    │       └── codeql-analysis.yml   <- configuration file for security scanning on Github Actions
    ├── Makefile                      <- Makefile with commands like `make lint` or `make build`
    ├── README.md                     <- The top-level README for developers using this project.
    ├── environment.yml               <- configuration file to create environment to run project on Binder
    ├── data
    │   ├── raw                       <- Scripts to download or generate data
    |   └── processed                 <- merged and filtered data, sampled at daily frequency
    ├── *.ipynb                       <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                                    and a short `-` delimited description, e.g. `1.0-jqp-initial-data-exploration`.
    ├── requirements.txt              <- base packages required to execute all Jupyter notebooks (incl. jupyter)
    ├── src                           <- Source code for use in this project.
    │   ├── __init__.py               <- Makes src a Python module
    │   └── *.py                      <- Scripts to use in analysis for pre-processing, visualization, training, etc.
    ├── papermill_runner.py           <- Python functions that execute system shell commands.
    └── tox.ini                       <- tox file with settings for running tox; see https://tox.readthedocs.io/en/latest/

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
