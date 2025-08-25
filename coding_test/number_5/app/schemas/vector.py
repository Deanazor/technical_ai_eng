from typing import Any
from pydantic import BaseModel


class VectorAddRequest(BaseModel):
    vector: list[float]
    text: str
    metadata: Any | None = None


class VectorSearchRequest(BaseModel):
    vector: list[float]


class VectorSearchResult(BaseModel):
    similarity: float
    text: str
    metadata: Any | None = None


class VectorSearchResponse(BaseModel):
    results: list[VectorSearchResult]
