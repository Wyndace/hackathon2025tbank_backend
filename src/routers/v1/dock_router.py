from fastapi import APIRouter, Query
from typing import List
from pydantic import BaseModel
from document_search import DocumentSearchEngine

search_engine = DocumentSearchEngine(documents_folder="./ebooks")

router = APIRouter()


class SearchResponse(BaseModel):
    filename: str
    similarity: float
    snippet: str | None
    metadata: dict


@router.get("/search", response_model=List[SearchResponse])
def search_documents(
    query: str = Query(..., min_length=3, description="Поисковый запрос"),
    top_n: int = Query(5, ge=1, le=20, description="Сколько результатов вернуть"),
):
    """
    Эндпоинт для поиска по библиотеке.
    """
    return search_engine.api_search(query, top_n=top_n)


@router.get("/documents")
def list_documents():
    """
    Получение всех загруженных документов с метаданными.
    """
    return search_engine.list_all_documents()
