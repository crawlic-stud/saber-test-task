from functools import partial

from fastapi import status
from pydantic import BaseModel


class AppExceptionModel(BaseModel):
    status_code: int
    detail: str
    message: str


class AppException(Exception):
    def __init__(self, status_code: int, detail: str, message: str) -> None:
        self.status_code = status_code
        self.detail = detail
        self.message = message


BadRequest = partial(AppException, status.HTTP_400_BAD_REQUEST)
NotFound = partial(AppException, status.HTTP_404_NOT_FOUND)
Forbidden = partial(AppException, status.HTTP_403_FORBIDDEN)
Conflict = partial(AppException, status.HTTP_409_CONFLICT)
InternalServerError = partial(AppException, status.HTTP_500_INTERNAL_SERVER_ERROR)
