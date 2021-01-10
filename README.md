This is a playground project to combine movies data with wiki info.
---------------------

### Contents

- [Docker Setup](#docker-setup)
- [Environment Setup](#environment-setup)
- [Data Linking and Ingestion](#data-linking-and-ingestion)
- [Query Data Using APIs](#query-data-using-restful-apis)

### Docker Setup

Instructions: 
1. Install [Docker](https://docs.docker.com/get-docker/)
1. Install [Docker Compose](https://docs.docker.com/compose/install/)

### Environment setup:
1. Build docker
    ```
    docker-compose build
    ```
1. Run docker service
    ```
    docker-compose up -d
    ```

### Data linking and ingestion

1. Run command to do Django migration to set up database schema
    ```
    docker-compose exec web python manage.py migrate
    ```
1. Run command to download movie and WIKI datasets
    ```
    docker-compose exec web python manage.py download_dataset
    ```
1. Run command to link movie with WIKI URL and abstract
    ```
    docker-compose exec web python manage.py run_movie_linking
    ```
1. Run command to ingestion data to database
    ```
    docker-compose exec web python manage.py movie_ingestion
    ```

### Query data using RESTFul APIs

After the setup with data linking and ingestion, the linked movie data shall be populated to the postgres database.

1. Query data using APIs
    Go to `http://localhost:8000/data/movies/` to see a list of movie data
1. Filter data
    The following fields can be used as url query to filter the list
    `budget, production_companies, revenue, rating, ratio, title, wiki_url, wiki_abstract, year`
    
    Query format: `/data/movies/?foo_field=<field_value>`
    
    Example: Query all movies rated 7.7.
    `http://localhost:8000/data/movies/?rating=7.7`

1. Search data
    Text or string fields are searchable.
    Search format `/data/movies/?search=<search_str>`
    
    Example: Search movies related to Disney.
    `http://localhost:8000/data/movies/?search=disney`
