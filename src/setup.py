import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from settings import log
from services.database import prepare_builds_and_tasks
from exceptions import AppException
from routes import tasks
from routes import builds


logging.basicConfig(level=log.LEVEL)
logger = logging.getLogger("api")


async def lifespan(_: FastAPI):
    try:
        await prepare_builds_and_tasks()
    except TypeError:
        raise RuntimeError(
            "Either builds/builds.yaml or builds/tasks.yaml is empty. Can not start the application."
        )
    yield


app = FastAPI(title="Build Master", lifespan=lifespan)
app.include_router(tasks.router)
app.include_router(builds.router)


@app.exception_handler(AppException)
async def handle_app_exception(_: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "message": exc.message},
    )
