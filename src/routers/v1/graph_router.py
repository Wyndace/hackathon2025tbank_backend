import networkx as nx
from fastapi import APIRouter

from src.shemas.route_shema import GraphRequest, PathNode, RouteResponse

graph_router = APIRouter()


@graph_router.post("/route", response_model=RouteResponse)
def find_path(data: GraphRequest, start_id: str, end_id: str) -> RouteResponse:
    g = nx.Graph()

    for node in data.nodes:
        g.add_node(node.id, x=node.x, y=node.y, floor=node.floor, type=node.type)

    for edge in data.edges:
        g.add_edge(edge.from_, edge.to, weight=edge.weight)

    path = nx.shortest_path(g, source=start_id, target=end_id, weight="weight")

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
