import asyncio
import logging

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

import exceptions
import settings
from models.task import Tasks
from models.build import Build, Builds, BuildGraph
from services.prepare_data import create_graph, prepare_tasks
from services.yaml_ops import read_tasks, read_builds


logger = logging.getLogger("db")
mongo_client = AsyncIOMotorClient(settings.db.get_url())
mongo_client.get_io_loop = asyncio.get_running_loop
db: AsyncIOMotorDatabase = mongo_client[settings.db.DB_NAME]

build_graphs_db: AsyncIOMotorCollection = db["build_graphs"]


async def upsert_build_graphs(
    builds: Builds, tasks_lookup: dict[str, list[str]]
) -> None:
    for build in builds.builds:
        build_graph = BuildGraph(
            name=build.name,
            tasks=build.tasks,
            graph=create_graph(build.tasks, tasks_lookup),
        )
        res = await build_graphs_db.update_one(
            {"name": build.name}, {"$set": build_graph.model_dump()}, upsert=True
        )
        logger.debug(f"Upserted_id: {res.upserted_id}, updated: {res.modified_count}")


async def get_build_by_name(name: str) -> BuildGraph:
    raw_build = await build_graphs_db.find_one({"name": name})
    if raw_build is None:
        raise exceptions.NotFound(
            detail=f"Build with {name=} wasn't found.",
            message="Ensure that this build exist or update YAML file in /builds",
        )
    return BuildGraph(**raw_build)


async def get_all_builds() -> list[Build]:
    cursor = build_graphs_db.find()
    result = []
    async for item in cursor:
        result.append(Build(**item))
    return result


async def prepare_builds_and_tasks(
    tasks: Tasks | None = None,
    builds: Builds | None = None,
) -> tuple[Builds, Tasks]:
    builds = read_builds() if not builds else builds
    tasks = read_tasks() if not tasks else tasks
    tasks_lookup = prepare_tasks(tasks.tasks)
    try:
        await upsert_build_graphs(builds, tasks_lookup)
    except KeyError as e:
        raise exceptions.BadRequest(
            detail=f"Unexpected task occured: {e}",
            message="Please ensure that you've added this task through PUT /tasks/yaml first",
        )
    await build_graphs_db.create_index("name")
    return builds, tasks
