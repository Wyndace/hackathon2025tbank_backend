from typing import Literal

from pydantic import BaseModel


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


class GraphRequest(BaseModel):
    nodes: list[Node]
    edges: list[Edge]


class PathNode(BaseModel):
    id: str
    x: float
    y: float
    floor: int
    type: Literal["cabinet", "corridor", "stairs", "toilet"]  # можно дополнять


class RouteResponse(BaseModel):
    path: list[PathNode]
