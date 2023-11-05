from fastapi import APIRouter, UploadFile, Depends, status

from models.build import Builds
from services.database import get_all_builds, prepare_builds_and_tasks
from services import docs
from services.yaml_ops import (
    BUILDS_PATH,
    verify_builds_yaml,
)
from exceptions import AppExceptionModel


router = APIRouter(prefix="/builds", tags=["Builds"])


@router.get(
    "",
    description=docs.create(
        "Returns all the builds that are available in the database"
    ),
)
async def get_builds() -> Builds:
    builds = await get_all_builds()
    return Builds(builds=builds)


@router.put(
    "/yaml",
    description=docs.create(
        "Replaces builds.yaml file",
    ),
    responses={status.HTTP_400_BAD_REQUEST: {"model": AppExceptionModel}},
)
async def put_builds_yaml_file(
    file: UploadFile = Depends(verify_builds_yaml),
) -> Builds:
    # after dependency injection we get bytes, not UploadFile
    BUILDS_PATH.write_bytes(file)
    builds, _ = await prepare_builds_and_tasks()
    return builds
