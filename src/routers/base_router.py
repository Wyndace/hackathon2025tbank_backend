from fastapi import APIRouter

from core.config import Settings
from src.routers.v1.graph_router import graph_router

base_router = APIRouter(prefix=Settings.API_VERSION)
base_router.include_router(graph_router)
