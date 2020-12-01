# 311 Chicago Incidents

[![Django CI](https://github.com/VangelisTsiatouras/311-chicago-incidents/workflows/Django%20CI/badge.svg)](https://github.com/VangelisTsiatouras/311-chicago-incidents/actions)  [![Vue.js CI](https://github.com/VangelisTsiatouras/311-chicago-incidents/workflows/Vue.js%20CI/badge.svg)](https://github.com/VangelisTsiatouras/311-chicago-incidents/actions)  [![codecov](https://codecov.io/gh/VangelisTsiatouras/311-chicago-incidents/branch/main/graph/badge.svg?token=2FOFQE6PH3)](https://codecov.io/gh/VangelisTsiatouras/311-chicago-incidents)

<img src="https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white"/>  <img src ="https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white"/>  <img src="https://img.shields.io/badge/vuejs%20-%2335495e.svg?&style=for-the-badge&logo=vue.js&logoColor=%234FC08D"/>

This repository contains 2 applications, DjangoREST &amp; Vue.js, that visualize some metrics &amp; stats for the incidents that happen to Chicago City.

All the data used for the development can be found [here](https://www.kaggle.com/chicago/chicago-311-service-requests
). Also I have uploaded some of these data inside this repository, which can be found [here](https://github.com/VangelisTsiatouras/311-chicago-incidents/tree/main/assist_material/datasets/zip).

## DjangoREST Application

### Installation from source

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
control. You can either set them at system level, or by creating a file named `.env` at the root of the repository. 
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
python manage.py createcachetable cache_table
```

and load the initial data with:

```bash
python manage.py import_incidents_from_csvs [csv_files]
```

where `csv_files` is the path of the csv files (one or more) to import to the database

_Example_
```bash
python manage.py import_incidents_from_csvs ../assist_material/datasets/csv/311-service-requests-abandoned-vehicles.csv ../assist_material/datasets/csv/311-service-requests-alley-lights-out.csv ../assist_material/datasets/csv/311-service-requests-pot-holes-reported.csv  
```

Now you can run the web server with:

```bash
python manage.py runserver
```

The API is available at http://127.0.0.1:8000/

## Vue.js Application

### Installation from source

First, [Yarn](https://classic.yarnpkg.com/en/docs/install/#debian-stable) should be installed on your machine. The
 following works for Ubuntu 20.04.

```bash
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install yarn
```

After, install all the dependencies of the application through Yarn package manager.

```bash
yarn install
```

### Compiles and hot-reloads for development
```bash
yarn serve
```

### Compiles and minifies for production
```bash
yarn build
```

### Lints and fixes files
```bash
yarn lint
```

## Installation using Docker

I have created Dockerfiles on both applications and with the `docker-compose.yml` you can build a database instance
, the Django API & the Vue.js client at the same time. I recommend this way of installation in order to keep your
 machine clean from packages that you may not use ever again. 
 
Initially, install [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) (click the link to see
 instructions) & [Docker Compose](https://docs.docker.com/compose/install/) in order to build the project.
 
__Set up the `.env` at the root of the repository!__
* `CHICAGO_INCIDENT_DATABASE_USER`: The database user
* `CHICAGO_INCIDENT_DATABASE_PASSWORD`: The database user password 
* `CHICAGO_INCIDENT_DATABASE_HOST`: `db` _The host name __must__ be `db`_
* `CHICAGO_INCIDENT_DATABASE_NAME`: The database name.

Then just execute the following:

```bash
docker-compose up --build
```

Then you have the database, the API & the Vue.js client up and running!

In order to perform the import of the data you can log in to the running docker container and perform the process
 manually. To do that, follow the instructions below.

Run:
```bash
docker ps
```

You will have in the output a table of all running docker containers of the project. Copy the `Containter ID` of the
image `311-chicago-incidents_api`.

After that log in to the container:
```bash
docker exec -t -i <CONTAINER_ID> bash
```

Now you have access to all the files of the API. __You can now run the import command as mentioned above in the Local
Development section.__

Also, it is recommended to create a superuser in order to have access to the `admin` the `swagger-documentation` pages.

Run
```bash
python manage.py createsuperuser
``` 

## Database Report

### Schema

![database-schema](https://github.com/VangelisTsiatouras/311-chicago-incidents/blob/main/assist_material/chicago_incident_development_schema_db.png)

### Queries

1. Find the total requests per type that were created within a specified time range and sort them in descending order.

    ```sql
    SELECT "incidents"."type_of_service_request", COUNT("incidents"."type_of_service_request") AS
    "number_of_requests" FROM "incidents" WHERE ("incidents"."creation_date" >= ? AND
    "incidents"."creation_date" <= ?) GROUP BY "incidents"."type_of_service_request"
    ORDER BY "number_of_requests" DESC;
    ```

    ```python
    queryset = Incident.objects.filter(creation_date__gte=data.get('start_date'),
                                       creation_date__lte=data.get('end_date')) \
       .values('type_of_service_request') \
       .annotate(number_of_requests=Count('type_of_service_request')) \
       .order_by('-number_of_requests')
    ```
    
2. Find the total requests per day for a specific request type and time range.

    ```sql
    SELECT "incidents"."creation_date", COUNT("incidents"."service_request_number") AS "number_of_requests"
    FROM "incidents" WHERE ("incidents"."creation_date" >= ? AND "incidents"."creation_date" <= ?
    AND "incidents"."type_of_service_request" = ?)
    GROUP BY "incidents"."creation_date" 
    ORDER BY "incidents"."creation_date" ASC;
    ```

    ```python
    queryset = Incident.objects.filter(type_of_service_request=data.get('type_of_service_request'),
                                       creation_date__gte=data.get('start_date'),
                                      creation_date__lte=data.get('end_date')) \
       .values('creation_date') \
       .annotate(number_of_requests=Count('service_request_number')) \
       .order_by('creation_date')
    ```

3. Find the most common service request per zipcode for a specific day.

    ```sql
    SELECT DISTINCT ON ("incidents"."zip_code") "incidents"."zip_code", "incidents"."type_of_service_request",
    COUNT("incidents"."type_of_service_request") AS "number_of_requests"
    FROM "incidents"
    WHERE "incidents"."zip_code" IS NOT NULL AND "incidents"."creation_date" = ?
    GROUP BY "incidents"."zip_code", "incidents"."type_of_service_request"
    ORDER BY "incidents"."zip_code", "number_of_requests" DESC
    ```

4. Find the average completion time per service request for a specific date range.

    ```sql
    SELECT "incidents"."type_of_service_request",
    AVG(("incidents"."completion_date" - "incidents"."creation_date")) AS "average_completion_time"
    FROM "incidents"
    WHERE ("incidents"."completion_date" IS NOT NULL
    AND "incidents"."creation_date" >= ?
    AND "incidents"."creation_date" <= ?)
    GROUP BY "incidents"."type_of_service_request"
    ORDER BY "incidents"."type_of_service_request" ASC
    ```

    ```python
    queryset = Incident.objects.filter(creation_date__gte=data.get('start_date'),
                                       creation_date__lte=data.get('end_date')) \
        .values('type_of_service_request') \
        .annotate(average_completion_time=Avg(F('completion_date') - F('creation_date'))) \
        .order_by('type_of_service_request')
    ```

5. Find the most common service request in a specified bounding box (as designated by GPS-
coordinates) for a specific day.

    ```sql
    SELECT "incidents"."type_of_service_request",
    COUNT("incidents"."type_of_service_request") AS "number_of_requests"
    FROM "incidents"
    WHERE ("incidents"."creation_date" = ? AND "incidents"."latitude" >= ?
    AND "incidents"."latitude" <= ? AND "incidents"."longitude" >= ?
    AND "incidents"."longitude" <= ?)
    GROUP BY "incidents"."type_of_service_request"
    ORDER BY "number_of_requests" DESC
    LIMIT 1
    ```

    ```python
    queryset = Incident.objects.filter(creation_date=data.get('date'),
                                       latitude__range=[data.get('b_latitude'), data.get('a_latitude')],
                                       longitude__range=[data.get('a_longitude'), data.get('b_longitude')]) \
        .values('type_of_service_request') \
        .annotate(number_of_requests=Count('type_of_service_request')) \
        .order_by('-number_of_requests')[:1]
    ```

6. Find the top-5 Special Service Areas (SSA) with regards to total number of requests per day
for a specific date range (for service requests types that SSA is available: abandoned vehicles,
garbage carts, graffiti removal, pot holes reported)

    ```sql
    SELECT "incidents"."ssa", COUNT("incidents"."service_request_number") AS "number_of_requests"
    FROM "incidents"
    WHERE ("incidents"."creation_date" >= %s AND "incidents"."creation_date" <= %s
    AND "incidents"."ssa" IS NOT NULL)
    GROUP BY "incidents"."ssa"
    ORDER BY "number_of_requests" DESC
    LIMIT 5
    ```

    ```python
    queryset = Incident.objects.filter(creation_date__gte=data.get('start_date'),
                                       creation_date__lte=data.get('end_date'),
                                       ssa__isnull=False) \
        .values('ssa') \
        .annotate(number_of_requests=Count('service_request_number')) \
        .order_by('-number_of_requests')[:5]
    ```

7. Find the license plates (if any) that have been involved in abandoned vehicle complaints more
than once.

    ```sql
    SELECT "abandoned_vehicles"."license_plate", COUNT(DISTINCT "incidents"."street_address") AS "number_of_requests"
    FROM "abandoned_vehicles"
    LEFT OUTER JOIN "abandoned_vehicles_incidents"
    ON ("abandoned_vehicles"."id" = "abandoned_vehicles_incidents"."abandoned_vehicle_id")
    LEFT OUTER JOIN "incidents"
    ON ("abandoned_vehicles_incidents"."incident_id" = "incidents"."id")
    WHERE "abandoned_vehicles"."license_plate" IS NOT NULL
    AND "incidents"."status" = 'OPEN'
    GROUP BY "abandoned_vehicles"."license_plate"
    HAVING COUNT(DISTINCT "incidents"."street_address") > 1;
    ```

8. Find the second most common color of vehicles involved in abandoned vehicle complaints.

    ```sql
    SELECT "abandoned_vehicles"."vehicle_color", COUNT("abandoned_vehicles"."vehicle_color") AS "color_count"
    FROM "abandoned_vehicles"
    WHERE "abandoned_vehicles"."vehicle_color" IS NOT NULL
    GROUP BY "abandoned_vehicles"."vehicle_color"
    ORDER BY "color_count" DESC
    LIMIT 1 OFFSET 1
    ```

    ```python
    queryset = AbandonedVehicle.objects.filter(vehicle_color__isnull=False) \
        .values('vehicle_color') \
        .annotate(color_count=Count('vehicle_color')) \
        .order_by('-color_count')[1:2]
    ```

9. Find the rodent baiting requests where the number of premises baited/rats/garbage is less than a specified
number.

    ```sql
    SELECT "incidents"."id", "incidents"."service_request_number", "incidents"."type_of_service_request",
    "incidents"."street_address", "incidents"."zip_code", "incidents"."latitude", "incidents"."longitude"
    FROM "incidents"
    INNER JOIN "rodent_baiting_premises"
    ON ("incidents"."id" = "rodent_baiting_premises"."incident_id")
    WHERE "rodent_baiting_premises"."number_of_premises_baited" < ?
    ```
   
10. For the Query 10 we can adapt the last line of the above query to the following
   
   ```sql
   WHERE "rodent_baiting_premises"."number_of_premises_w_garbage" < ?
   ```
   
11. Similar for Query 11
    ```sql
    WHERE "rodent_baiting_premises"."number_of_premises_w_rats" < ?
    ```
    
    Combined all together to one Django ORM query:

    ```python
    queryset = Incident.objects.values('id', 'service_request_number', 'type_of_service_request',
                                       'street_address', 'zip_code', 'latitude', 'longitude')
    if type_of_premises == serializers.RodentBaitingParams.BAITED:
        queryset = queryset.filter(rodent_baiting_premises__number_of_premises_baited__lt=data.get('threshold')) \
            .order_by('id')
    elif type_of_premises == serializers.RodentBaitingParams.GARBAGE:
        queryset = queryset.filter(rodent_baiting_premises__number_of_premises_w_garbage__lt=data
                                   .get('threshold')) \
            .order_by('id')
    elif type_of_premises == serializers.RodentBaitingParams.RATS:
        queryset = queryset.filter(rodent_baiting_premises__number_of_premises_w_rats__lt=data.get('threshold')) \
            .order_by('id')
    ```

12. Find the police districts that have handled “pot holes” requests with more than one number
of potholes on the same day that they also handled “rodent baiting” requests with more than
one number of premises baited, for a specific day.

    ```sql
    SELECT "incidents"."police_district",
    SUM("rodent_baiting_premises"."number_of_premises_baited") AS "rodent_baiting_sum",
    SUM("number_of_carts_and_potholes"."number_of_elements") AS "potholes_sum"
    FROM "incidents"
    LEFT OUTER JOIN "rodent_baiting_premises"
    ON ("incidents"."id" = "rodent_baiting_premises"."incident_id")
    LEFT OUTER JOIN "number_of_carts_and_potholes"
    ON ("incidents"."id" = "number_of_carts_and_potholes"."incident_id")
    WHERE ("incidents"."completion_date" = ?
    AND
    ("incidents"."type_of_service_request" = 'RODENT_BAITING' OR
    "incidents"."type_of_service_request" = 'POT_HOLE'))
    GROUP BY "incidents"."police_district"
    HAVING
    (SUM("number_of_carts_and_potholes"."number_of_elements") > 1
    AND SUM("rodent_baiting_premises"."number_of_premises_baited") > 1)
    ORDER BY "incidents"."police_district" ASC
    ```
    
    ```python
    queryset = Incident.objects.filter(Q(completion_date=data.get('date')) & (
            Q(type_of_service_request=Incident.RODENT_BAITING) | Q(type_of_service_request=Incident.POT_HOLE))) \
        .values('police_district') \
        .annotate(rodent_baiting_sum=Sum('rodent_baiting_premises__number_of_premises_baited'),
                  potholes_sum=Sum('number_of_carts_and_potholes__number_of_elements')) \
        .filter(rodent_baiting_sum__gt=1, potholes_sum__gt=1) \
        .order_by('police_district')
    ```
