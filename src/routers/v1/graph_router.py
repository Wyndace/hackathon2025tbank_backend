import networkx as nx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.connection import get_db
from src.repositories.graph import GraphsMapRepo
from src.shemas.route_shema import GraphRequest, PathNode, RouteRequest, RouteResponse

graph_router = APIRouter(prefix="/graph", tags=["graph"])


@graph_router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
async def upload_graph(
    data: GraphRequest,
    university: str,
    db: AsyncSession = Depends(get_db)
) -> None:
    return await GraphsMapRepo.upload_graph(db, university, data.model_dump())


@graph_router.post(
    "/route",
    response_model=RouteResponse
)
async def find_path(
    query: RouteRequest,
    db: AsyncSession = Depends(get_db)
) -> RouteResponse:
    graph_row = await GraphsMapRepo.get_by_address(
        db=db,
        address=query.address
    )

    if not graph_row:
        raise HTTPException(status_code=404, detail="Graph not found")

    graph_data = graph_row.graph
    g = nx.Graph()

    for node in graph_data["nodes"]:
        g.add_node(
            node["id"],
            x=node["x"],
            y=node["y"],
            floor=node["floor"],
            type=node["type"]
        )

    for edge in graph_data["edges"]:
        g.add_edge(edge["from"], edge["to"], weight=edge["weight"])

    try:
        path = nx.shortest_path(
            g, source=query.start_id, target=query.end_id, weight="weight"
        )
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=400, detail="No path found")

    coords = [
        PathNode(
            id=n,
            x=g.nodes[n]["x"],
            y=g.nodes[n]["y"],
            floor=g.nodes[n]["floor"],
            type=g.nodes[n]["type"]
        )
        for n in path
    ]

    return RouteResponse(path=coords)
