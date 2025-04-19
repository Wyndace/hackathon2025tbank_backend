from fastapi import APIRouter

from core.config import Settings

base_router = APIRouter(prefix=Settings.API_VERSION)

