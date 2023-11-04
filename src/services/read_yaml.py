from pathlib import Path
from typing import Any

import yaml

from models.task import Tasks
from models.build import Builds


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
