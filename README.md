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

## [About](#about)
### [Company](#company)
Forecast six-weeks ahead store-wise sales for [Rossmann drug store chain in Germany](https://en.wikipedia.org/wiki/Rossmann_(company)).

### [Forecasting Sales](#forecasting-sales)
Sales planning is important for companies in a high growth mode or those that are in the process of adding new products or entering into new markets.

For Rossmann, a sales forecast can have tremendous value across the entire chain of drug stores. Storewide forecasts could play an important role in operational efficiency of each individual store. Store managers, citywide/statewide/regional managers and strategic planners can use a sales forecast to design and implement sales and operational policies that maximize storewide sales revenue.

### [Current Use-Case](#current-use-case)
In the retail shopping industry, the problem of overstaffing can be a significant contributor to increased costs while understaffing can negatively impact customer satisfaction. In an attempt to help deal with these issues, as part of a strategic planning initiative designed to assist store managers with staffing arrangements, the company is looking to forecast daily store sales for a six week (1.5 months) ahead period corresponding to Aug 1, 2015 to September 17, 2015 at approximately 1,100 of the nearly 2,000 ([1](http://www.cosmetic-business.com/de/News/rossmann-continues-to-grow/381871), [2](https://www.statista.com/statistics/717960/rossmann-stores-germany/)) Rossmann stores in Germany.

Such a forecast facilitates the following
-   better staffing schedule planning in order to match number of employees servicing a single store with expected sales in that store
-   create effective staff schedules that increase productivity and motivation
-   optimal balance between the customer satisfaction and wage expense

and will help store managers stay focused on their customers and their teams.

Due to the frequency of changes in sales data, a forecast designed using historical data upto the end of 2014 might not be valid deep into 2015. So, Rossmann has picked a forecast period that is not long enough to span several months of but is also sufficiently long that store managers will consult the forecast to create meaningful staffing rotas which will more accurately meet expected customer demand than rules-based or naive forecasting techniques during this period of the year.

In-store sales are affected by numerous factors, including store location, competitors, seasonality, in-store promotions and school/state holidays. This period of the year is unique in that it covers the latter half of the current academic year's school holidays and the start of the following year's school year. However, the exact dates of school holidays vary by states in Germany ([1](https://study.studentnews.eu/s/3693/75527-School-year-in-Europe/4084760-Germany-201516.htm)). Upto five public holidays also cover this period, depending on the state ([1](https://www.timeanddate.com/holidays/germany/2015)). Student employment at stores naturally rises during the school vacation and drops off when the school semester resumes - this impacts store managers staffing schedules during this period, and a reliable forecast will aid in creating schedules that reflect sales generated without negatively impacting customer satisfaction.

### [Requirements](#requirements)
The requirement of the forecast is that it be available to store managers on the first day of this period (i.e. on August 1, 2015) so that they can use it to plan store staffing operations (hiring and scheduling) over the following six weeks starting from that date (Aug 1, 2015). Also, data to be used to generate a forecast ends on July 25, 2015. This means that the forecast must be developed during the period (gap) of July 26, 2015 to July 31, 2015.

### [Objective](#objective)
Forecast store-wise sales for approximately 1,100 of the German-based stores in the Rossmann chain over the period of Aug 1, 2015 to Sep 17, 2015.

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
