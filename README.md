# saber-test-task

Test task from [Saber](https://saber.games/)

## Description

Application that provides a microservice to get all dependencies for building the game. Tasks are sorted using [Kahn&#39;s topological sort algorithm](https://en.wikipedia.org/wiki/Topological_sorting). All interactions go through FastAPI app, that handles requests and MongoDB, that stores graph data for each build.

## Technologies used:

- FastAPI
- Pydantic 2
- MongoDB (motor)
- pyYAML

## How to run:

1. With docker-compose:

```sh
docker-compose up
```

2. With existing database (need to change .env file)

```sh
python src/main.py
```

## Contacts:

- [Telegram](https://t.me/crawlic)
- E-mail: nikitosik0726@gmail.com
