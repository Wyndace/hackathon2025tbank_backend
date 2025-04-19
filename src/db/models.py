from sqlalchemy import (
    JSON,
    Column,
    Integer,
    MetaData,
    String,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base(metadata=MetaData())


class GraphsMap(Base):
    __tablename__ = "graphs_maps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    university = Column(String, nullable=False)
    address = Column(String, nullable=False, unique=True)
    graph = Column(JSON, nullable=False)
