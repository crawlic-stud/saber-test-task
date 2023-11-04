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

0. Copy ``.env.example`` to ``.env`` and replace placeholder values (if needed)
1. Run with docker-compose:

```sh
docker-compose up
```

---

If you have an existing database (need to change .env file)

```sh
python src/main.py
```

or with docker-compose:

```sh
docker-compose up prod
```

## Contacts:

- [Telegram](https://t.me/crawlic)
- E-mail: nikitosik0726@gmail.com
