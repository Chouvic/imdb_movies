This is a playground project to combine movies data with wiki info.
---------------------

 * Introduction
 * How to use
 * Recommended modules
 
 
INTRODUCTION
------------

This is a need to match the movies data with wiki pages information.

How to use
------------


### Development Setup

Instructions: 
1. Install python3
1. Install [Docker](https://docs.docker.com/get-docker/)
1. Install [Docker Compose](https://docs.docker.com/compose/install/)

### Environment setup:
1. Start a virtual environment
    ```
    python3 -m venv venv/
    ```
1. Activate the virtual environment
    ```
    source venv/bin/activate
    ```
1. Install required packages
    ```
    pip install -r requirements.txt
    ```
1. Run Django migration to set up database schema
    ```
    python manage.py migrate
    ```

### Data linking and ingestion

1. Run command to download movie and WIKI datasets
    ```
    python manage.py download_dataset
    ```
1. Run command to link movie with WIKI URL and abstract
    ```
    python manage.py run_movie_linking
    ```
1. Run command to ingestion data to database
    ```
    python manage.py movie_ingestion
    ```

### Start the DEV server and query data

1. Start DEV server
    ```
    python manage.py runserver
    ```
1. Query data using APIs
    Go to `localhost:8000` to see a list of movie data
