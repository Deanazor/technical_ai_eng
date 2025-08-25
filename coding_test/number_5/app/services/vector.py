import asyncio
import math


from app.schemas.vector import (
    VectorAddRequest,
    VectorSearchResponse,
    VectorSearchResult,
    VectorSearchRequest,
)


class VectorDB:
    def __init__(self):
        self.vectors = []
        self.texts = []
        self.metadata = []
        self.vector_dim = None

    def _dot_product(self, vector1: list, vector2: list) -> float:
        return sum(a * b for a, b in zip(vector1, vector2))

    def _vector_len(self, vector: list) -> float:
        return math.sqrt(self._dot_product(vector, vector))

    def _cosine_similarity(self, vector1: list, vector2: list) -> float:
        return self._dot_product(vector1, vector2) / (
            self._vector_len(vector1) * self._vector_len(vector2)
        )

    def add_vector(self, request: VectorAddRequest):
        if self.vector_dim is None:
            self.vector_dim = len(request.vector)
        elif len(request.vector) != self.vector_dim:
            raise ValueError(
                f"Vector dimension mismatch: expected {self.vector_dim}, got {len(request.vector)}"
            )

        self.vectors.append(request.vector)
        self.texts.append(request.text)
        self.metadata.append(request.metadata)

    async def search(
        self, request: VectorSearchRequest, top_k: int = 5
    ) -> VectorSearchResponse:
        if not self.vectors:
            return VectorSearchResponse(results=[])

        calculation_tasks = [
            asyncio.to_thread(self._cosine_similarity, vector, request.vector)
            for vector in self.vectors
        ]
        similarities = await asyncio.gather(*calculation_tasks)

        top_indices = sorted(
            range(len(similarities)), key=lambda i: similarities[i], reverse=True
        )[:top_k]

        results = [
            VectorSearchResult(
                similarity=similarities[idx],
                text=self.texts[idx],
                metadata=self.metadata[idx],
            )
            for idx in top_indices
        ]

        return VectorSearchResponse(results=results)
