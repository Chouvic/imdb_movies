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


### Future tasks

1. Linking between movie and wiki title

    As there is no exact match between IMDB movies and WIKI XML content, the current solution just compared 
    the movie title with the title content in each component of the XML file. Thus, the use of movie title
    to find its related wiki page is not reliable although it is a good starting point.
    To improve the accuracy of mapping, additional methods to find exact match is needed.

1. Parsing performance
    
    When parsing the large XML file, only one tag object is read at one time thus it can reduce the memory load. 
    The tag object will be deleted once it has been read and processed.
    However, the current parser just used one process and thread to parse the large XML file, the performance can be
    improved by using multiple threads and coroutine to reduce the IO time.

1. Tools: Big files handling
    
    In this project, Django and Django RestFrameWork are used to provide APIs services. Its 
    Object-Relational Mapper is generic so that it supports different types of databases.
    Also, building models and data ingestion are very quick to apply with Django.

    Dockerization methods are applied to ease the deployment effort.

    Now, only several GB scale data is being parsed. It will be an issue once the scale 
    of file raised to hundred or TB level. In such scenario, Hadoop can be applied with multiple nodes.
    It will boost up the speed by splitting the big files to multiple small blocks(E.g. 128 MB). In
    the meantime, MapReduce can be applied to process the files in parallel.

1. Testing
    
    Testing can be applied based on following aspects: 
    1. Check whether files are downloaded once a download command is initiated.
    1. Ensure the parsed CSV has its linking fields attached. 
    1. APIs can be tested to check its data after movie ingestion is done. 
    1. End to end tests can be added once the server is set up after ingesting movie data.
