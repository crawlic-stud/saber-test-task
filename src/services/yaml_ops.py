import io
from pathlib import Path
from typing import Any, BinaryIO

from fastapi import UploadFile
import yaml
from pydantic import ValidationError

from models.task import Tasks
from models.build import Builds
import exceptions


TASKS_PATH = Path.cwd() / "builds" / "tasks.yaml"
BUILDS_PATH = Path.cwd() / "builds" / "builds.yaml"


def read_yaml_from_path(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data


def read_tasks() -> Tasks:
    data = read_yaml_from_path(TASKS_PATH)
    return Tasks(**data)


def read_builds() -> Builds:
    data = read_yaml_from_path(BUILDS_PATH)
    return Builds(**data)


async def verify_yaml_structure(
    model: type[Tasks] | type[Builds],
    file: UploadFile,
) -> bytes:
    if not file.filename.endswith(".yaml"):
        raise exceptions.BadRequest(
            detail=f"Expected a .yaml file, not .{file.filename.split('.')[-1]} file",
            message="Ensure that you are sending a correct YAML file.",
        )
    try:
        file_bytes = await file.read()
        data = yaml.safe_load(file_bytes)
        _ = model(**data)
    except (ValidationError, TypeError):
        raise exceptions.BadRequest(
            detail=f"Structure doesn't correspond to {model.__name__} structure",
            message="Ensure that the structure is correct and try again.",
        )
    return file_bytes


async def verify_builds_yaml(file: UploadFile):
    return await verify_yaml_structure(Builds, file)


async def verify_tasks_yaml(file: UploadFile):
    return await verify_yaml_structure(Tasks, file)
