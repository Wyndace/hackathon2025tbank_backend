from typing import Literal

from pydantic import BaseModel, ConfigDict


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
