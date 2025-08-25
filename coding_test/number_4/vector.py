import asyncio
import math
from typing import Any


class VectorDB:
    def __init__(self):
        self.vectors = []
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

    def add_vector(self, vector: list, metadata: Any = None):
        if self.vector_dim is None:
            self.vector_dim = len(vector)
        elif len(vector) != self.vector_dim:
            raise ValueError(f"Vector dimension mismatch: expected {self.vector_dim}, got {len(vector)}")

        self.vectors.append(vector)
        self.metadata.append(metadata)

    async def search(self, query_vector: list, top_k: int = 5) -> list[tuple[float, Any]]:
        if not self.vectors:
            return []

        calculation_tasks = [
            asyncio.to_thread(self._cosine_similarity, vector, query_vector)
            for vector in self.vectors
        ]
        similarities = await asyncio.gather(*calculation_tasks)

        top_indices = sorted(
            range(len(similarities)), key=lambda i: similarities[i], reverse=True
        )[:top_k]

        results = []
        for idx in top_indices:
            results.append((similarities[idx], self.metadata[idx]))

        return results
