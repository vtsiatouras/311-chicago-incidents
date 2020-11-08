# 311 Chicago Incidents

[![Django CI](https://github.com/VangelisTsiatouras/311-chicago-incidents/workflows/Django%20CI/badge.svg)](https://github.com/VangelisTsiatouras/311-chicago-incidents/actions)

[![codecov](https://codecov.io/gh/VangelisTsiatouras/311-chicago-incidents/branch/main/graph/badge.svg?token=2FOFQE6PH3)](https://codecov.io/gh/VangelisTsiatouras/311-chicago-incidents)

<img src="https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white"/>

<img src ="https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white"/>

This repository contains 2 applications, DjangoREST &amp; Vue.js, that visualize some metrics &amp; stats for the incidents that happen to Chicago City.

All the data used for the development can be found [here](https://www.kaggle.com/chicago/chicago-311-service-requests
). Also I have uploaded some of these data inside this repository, which can be found [here](https://github.com/VangelisTsiatouras/311-chicago-incidents/tree/main/assist_material/datasets/zip).

## DjangoREST Application

### Installation

This section contains the installation instructions in order to set up a local development environment. The instructions
have been validated for Ubuntu 20.04.

First, install all required software with the following command:

```bash
sudo apt update
sudo apt install git python3 python3-pip python3-dev postgresql postgresql-contrib 
```

The project dependencies are managed with [pipenv](https://docs.pipenv.org/en/latest/). You can install it with:

```bash
pip install --user pipenv
```

`pipenv` should now be in your `PATH`. If not, logout and log in again. Then install all dependencies with:

```bash
pipenv install --dev
```

Then you can enable the python environment with:

```bash
pipenv shell
```

All commands from this point forward require the python environment to be enabled.

### Environment variables

The project uses environment variables in order to keep private data like user names and passwords out of source
control. You can either set them at system level, or by creating a file named `.env` at the project root (`backend/`). 
The required environment variables for development are:

* `CHICAGO_INCIDENT_DATABASE_USER`: The database user
* `CHICAGO_INCIDENT_DATABASE_PASSWORD`: The database user password 
* `CHICAGO_INCIDENT_DATABASE_HOST`: The database host. _For local development use_
 `localhost`
* `CHICAGO_INCIDENT_DATABASE_NAME`: The database name.

### Local Development
In order to run the project on your workstation, you must create a database named according to the value of the
`CHICAGO_INCIDENT_DATABASE_NAME` environment variable, at the host that is specified by the
`CHICAGO_INCIDENT_DATABASE_HOST` environment variable. You can create the database by running:

```
sudo -u postgres psql
postgres=# CREATE DATABASE chicago_incident_development_db;
```

After you create the database, you can populate it with the initial schema by running:

```bash
python manage.py migrate
```

and load the initial data with:

```bash
python manage.py import_incidents_from_csvs csv_file
```

where `csv_file` is the path of the csv dataset

Now you can run the web server with:

```bash
python manage.py runserver
```

The API is available at http://127.0.0.1:8000/
