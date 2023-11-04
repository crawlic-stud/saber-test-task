from pydantic import BaseModel


class Task(BaseModel):
    name: str
    dependencies: list[str]


class Tasks(BaseModel):
    tasks: list[Task]
