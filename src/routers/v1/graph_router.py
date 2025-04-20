import asyncio

import networkx as nx
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.connection import get_db
from src.repositories.graph import GraphsMapRepo
from src.scripts.minio_client import get_from_minio, upload_to_minio
from src.shemas.graph_shema import GraphRequest, GraphUpdateRequest, PhotoURLS
from src.shemas.route_shema import PathNode, RouteRequest, RouteResponse

graph_router = APIRouter(prefix="/graph", tags=["graph"])


@graph_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
async def upload_graph(
    data: GraphRequest,
    db: AsyncSession = Depends(get_db)
) -> None:
    return await GraphsMapRepo.upload_graph(db, data.model_dump())


@graph_router.post(
    "/photos",
    status_code=status.HTTP_201_CREATED,
    response_model=PhotoURLS,
)
async def upload_photos(
    data: list[UploadFile] = File(...),
) -> PhotoURLS:
    for file in data:
        contents = await file.read()
        await upload_to_minio(contents, file.filename)
    urls = await asyncio.gather(*[
        get_from_minio(file.filename) for file in data
    ])

    return PhotoURLS(urls=urls)


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


@graph_router.get("/")
async def get_all_graphs(db: AsyncSession = Depends(get_db)):
    graphs = await GraphsMapRepo.get_all(db)
    return [
        {
            "id": g.id,
            "university": g.university,
            "address": g.address
        } for g in graphs
    ]


@graph_router.delete("/{address}")
async def delete_graph(address: str, db: AsyncSession = Depends(get_db)):
    await GraphsMapRepo.delete_by_address(db, address)
    return {"status": "ok", "message": f"Graph with address '{address}' deleted"}


@graph_router.put("/")
async def update_graph(
    data: GraphUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    update_data = {}
    if data.university:
        update_data["university"] = data.university
    if data.graph:
        update_data["graph"] = data.graph.model_dump()

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    await GraphsMapRepo.update_by_address(db, address=data.address, new_data=update_data)
    return {"status": "ok", "message": "Graph updated"}
