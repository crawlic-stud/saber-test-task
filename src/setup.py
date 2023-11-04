import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from settings import log
from services.read_yaml import read_tasks, read_builds
from services.prepare_data import prepare_tasks
from services.database import upsert_build_graphs, build_graphs_db
from exceptions import AppException
from routes import tasks


logging.basicConfig(level=log.LEVEL)


async def lifespan(_: FastAPI):
    builds = read_builds()
    tasks = read_tasks()
    tasks_lookup = prepare_tasks(tasks.tasks)
    await upsert_build_graphs(builds, tasks_lookup)
    await build_graphs_db.create_index("name")
    yield


app = FastAPI(title="Build Master", lifespan=lifespan)
app.include_router(tasks.router)


@app.exception_handler(AppException)
async def handle_app_exception(_: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "message": exc.message},
    )
