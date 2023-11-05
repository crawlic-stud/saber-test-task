# Saber's Test Task

Test task from [Saber](https://saber.games/)

## Description

Application that provides a microservice to get all dependencies for building the game. Tasks are sorted using [Kahn&#39;s topological sort algorithm](https://en.wikipedia.org/wiki/Topological_sorting). All interactions go through FastAPI app, that handles requests and MongoDB, that stores graph data for each build to minimize compute time needed. 

## Technologies used:

- FastAPI
- uvicorn
- Pydantic 2
- MongoDB (motor)
- pyYAML
- Docker + Docker Compose
- Pytest


## How to run:

0. Copy ``.env.example`` to ``.env`` and replace placeholder values (if needed)
1. Run with docker-compose:

```sh
docker-compose up
```

---

To run with an existing database (need to change ```MONGO_``` fields in .env file)

```sh
python src/main.py
```

or same with docker-compose:

```sh
docker-compose up prod
```

## Run tests:

```sh
pip install pytest
pytest src
```

## API description:

 - To view API documentation visit ```http://0.0.0.0:8000/docs``` (by default)
 - To retrieve tasks for certain build use ```GET /tasks/{build_name}```
 - To list all available builds use ```GET /builds```
 - To update ```tasks.yaml``` or ```builds.yaml``` files use ```PUT /tasks/yaml``` and ```PUT /builds/yaml``` respectively

## Possible future improvements:

1. Add CRUD operations to ```/tasks``` and ```/builds```, so we don't have to rely on ```.yaml``` files as the source of truth
2. Add auth to API endpoints to ensure safety of data
3. Add more test cases to test important functionality of API's endpoints
4. Add logging to the core functionality

## Contacts:

- [Telegram](https://t.me/crawlic)
- E-mail: nikitosik0726@gmail.com
