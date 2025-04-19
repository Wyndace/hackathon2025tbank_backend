from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import GraphsMap


class GraphsMapRepo:

    @staticmethod
    async def upload_graph(db: AsyncSession, university: str, address: str, data: dict) -> None:
        existing = await GraphsMapRepo.get_by_address(db, address)
        if existing:
            raise HTTPException(status_code=409, detail="Graph for this address has already been set")

        graph_obj = GraphsMap(
            university=university,
            address=address,
            graph=data
        )
        db.add(graph_obj)
        await db.commit()
        return

    @staticmethod
    async def get_by_address(db: AsyncSession, address: str) -> GraphsMap | None:
        result = await db.execute(
            select(GraphsMap).where(GraphsMap.address == address)
        )
        return result.scalar_one_or_none()
