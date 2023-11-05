from fastapi import APIRouter, status, Depends, UploadFile

from services.database import get_build_by_name, prepare_builds_and_tasks
from services.topological_sort import kahn_topsort
from services import docs
from exceptions import AppExceptionModel
from models.task import Tasks
from services.yaml_ops import TASKS_PATH, verify_tasks_yaml, read_tasks


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get(
    "/{build_name}",
    description=docs.create(
        "Returns all tasks that are needed to complete the build",
        notes=[
            "Returns all tasks in ```topological order```",
            "Field ```build_name``` is required",
        ],
        usage="Provide ```build_name``` in url and get list of task names",
    ),
    responses={status.HTTP_404_NOT_FOUND: {"model": AppExceptionModel}},
)
async def get_tasks_for_build(build_name: str) -> list[str]:
    build_graph = await get_build_by_name(build_name)
    tasks = kahn_topsort(build_graph.graph)
    return tasks


@router.put(
    "/yaml",
    description=docs.create(
        "Replaces tasks.yaml file",
    ),
    responses={status.HTTP_400_BAD_REQUEST: {"model": AppExceptionModel}},
)
async def put_tasks_yaml_file(
    file: UploadFile = Depends(verify_tasks_yaml),
) -> Tasks:
    # after dependency we get bytes, not UploadFile
    TASKS_PATH.write_bytes(file)
    _, tasks = await prepare_builds_and_tasks()
    return tasks
