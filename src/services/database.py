import asyncio
import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from settings import db
from models.build import Builds, BuildGraph
from services.prepare_data import create_graph
import exceptions


logger = logging.getLogger("db")
mongo_client = AsyncIOMotorClient(db.get_url())
mongo_client.get_io_loop = asyncio.get_running_loop
db: AsyncIOMotorCollection = mongo_client[db.DB_NAME]

build_graphs_db = db["build_graphs"]


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
            message="Ensure that this build exist or update YAML file via POST /api/builds/yaml",
        )
    return BuildGraph(**raw_build)
