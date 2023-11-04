from fastapi import APIRouter, status

from services.database import get_build_by_name
from services.topological_sort import kahn_topsort
from services import docs
from exceptions import AppExceptionModel


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
