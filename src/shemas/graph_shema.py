
from pydantic import BaseModel, ConfigDict


class Node(BaseModel):
    id: str
    x: float
    y: float
    type: str  # cabinet, corridor, stairs
    floor: int


class Edge(BaseModel):
    from_: str
    to: str
    weight: float


class Graph(BaseModel):
    nodes: list[Node]
    edges: list[Edge]


class GraphRequest(BaseModel):
    graph: Graph
    university: str
    address: str

    model_config = ConfigDict(from_attributes=True)


class GraphUpdateRequest(BaseModel):
    address: str
    university: str | None = None
    graph: Graph | None = None
