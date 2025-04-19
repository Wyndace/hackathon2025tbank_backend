from typing import Literal

from pydantic import BaseModel, ConfigDict


class Node(BaseModel):
    id: str
    x: float
    y: float
    type: str  # cabinet, corridor, stairs
    floor: int

    model_config = ConfigDict(from_attributes=True)


class Edge(BaseModel):
    from_: str
    to: str
    weight: float

    model_config = ConfigDict(from_attributes=True)


class GraphRequest(BaseModel):
    nodes: list[Node]
    edges: list[Edge]

    model_config = ConfigDict(from_attributes=True)


class PathNode(BaseModel):
    id: str
    x: float
    y: float
    floor: int
    type: Literal["cabinet", "corridor", "stairs", "toilet"]  # можно дополнять

    model_config = ConfigDict(from_attributes=True)


class RouteResponse(BaseModel):
    path: list[PathNode]

    model_config = ConfigDict(from_attributes=True)


class RouteRequest(BaseModel):
    address: str
    start_id: str
    end_id: str

    model_config = ConfigDict(from_attributes=True)
