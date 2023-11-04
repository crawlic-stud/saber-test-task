from pydantic import BaseModel, Field


class Build(BaseModel):
    name: str
    tasks: list[str]


class Builds(BaseModel):
    builds: list[Build]


class BuildGraphNode(BaseModel):
    degree: int
    nodes: list[str]


class BuildGraph(Build):
    graph: dict[str, BuildGraphNode] = Field(default_factory=dict)
