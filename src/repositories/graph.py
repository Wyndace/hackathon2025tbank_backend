from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import GraphsMap


class GraphsMapRepo:

    @staticmethod
    async def upload_graph(db: AsyncSession, data: dict) -> None:
        if await GraphsMapRepo.get_by_address(db, data.get("address", "")):
            raise HTTPException(status_code=409, detail="Graph for this address has already been set")

        db.add(GraphsMap(**data))
        await db.commit()
        return

    @staticmethod
    async def get_by_address(db: AsyncSession, address: str) -> GraphsMap | None:
        result = await db.execute(
            select(GraphsMap).where(GraphsMap.address == address)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession) -> Sequence[GraphsMap]:
        result = await db.execute(select(GraphsMap))
        return result.scalars().all()

    @staticmethod
    async def delete_by_address(db: AsyncSession, address: str) -> None:
        result = await db.execute(
            select(GraphsMap).where(GraphsMap.address == address)
        )
        graph = result.scalar_one_or_none()
        if not graph:
            raise HTTPException(status_code=404, detail="Graph not found")
        await db.delete(graph)
        await db.commit()

    @staticmethod
    async def update_by_address(db: AsyncSession, address: str, new_data: dict) -> None:
        graph = await GraphsMapRepo.get_by_address(db, address)
        if not graph:
            raise HTTPException(status_code=404, detail="Graph not found")
        for key, value in new_data.items():
            setattr(graph, key, value)
        await db.commit()
