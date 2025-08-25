import pytest
from vector import VectorDB


def test_init():
    """Test VectorDB initialization"""
    db = VectorDB()
    assert db.vectors == []
    assert db.metadata == []
    assert db.vector_dim is None


@pytest.mark.parametrize(
    "vector1, vector2, expected",
    [
        ([1, 2, 3], [4, 5, 6], 1 * 4 + 2 * 5 + 3 * 6),
        ([1, 2, 3], [0, 0, 0], 0),
        ([1, 2, 3], [-1, -2, -3], 1 * (-1) + 2 * (-2) + 3 * (-3)),
        ([5], [3], 15),
        ([], [], 0),
    ],
)
def test_dot_product(vector1, vector2, expected):
    db = VectorDB()
    result = db._dot_product(vector1, vector2)
    assert result == expected


@pytest.mark.parametrize(
    "vector, expected",
    [
        ([3, 4], 5.0),
        ([5], 5.0),
        ([0, 0, 0], 0.0),
        ([1, 0, 0], 1.0),
        ([-3, -4], 5.0),
        ([], 0.0),
    ],
)
def test_vector_len(vector, expected):
    db = VectorDB()
    result = db._vector_len(vector)
    assert result == expected


@pytest.mark.parametrize(
    "vector1, vector2, expected",
    [
        ([1, 2, 3], [1, 2, 3], 1.0),
        ([1, 0], [0, 1], 0.0),
        ([1, 0], [-1, 0], -1.0),
        ([1, 2, 3], [2, 4, 6], 1.0),
    ],
)
def test_cosine_similarity(vector1, vector2, expected):
    db = VectorDB()
    result = db._cosine_similarity(vector1, vector2)
    assert abs(result - expected) < 1e-10


def test_cosine_similarity_zero_vector():
    db = VectorDB()

    vector = [1, 2, 3]
    zero_vector = [0, 0, 0]

    with pytest.raises(ZeroDivisionError):
        db._cosine_similarity(vector, zero_vector)

    with pytest.raises(ZeroDivisionError):
        db._cosine_similarity(zero_vector, vector)


def test_add_vector_first_time():
    db = VectorDB()

    vector = [1, 2, 3]
    metadata = "doc1"

    db.add_vector(vector, metadata)

    assert db.vectors == [vector]
    assert db.metadata == [metadata]
    assert db.vector_dim == 3


def test_add_vector_multiple():
    db = VectorDB()

    db.add_vector([1, 2, 3], "doc1")
    db.add_vector([4, 5, 6], "doc2")

    db.add_vector([7, 8, 9], "doc3")

    expected_vectors = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    expected_metadata = ["doc1", "doc2", "doc3"]

    assert db.vectors == expected_vectors
    assert db.metadata == expected_metadata
    assert db.vector_dim == 3


def test_add_vector_empty_vector():
    db = VectorDB()

    db.add_vector([], "empty_doc")

    assert db.vectors == [[]]
    assert db.metadata == ["empty_doc"]
    assert db.vector_dim == 0


def test_add_vector_dimension_mismatch():
    db = VectorDB()

    db.add_vector([1, 2, 3], "doc1")

    with pytest.raises(ValueError, match="Vector dimension mismatch"):
        db.add_vector([4, 5], "doc2")

    db.add_vector([4, 5, 6], "doc2")
    assert len(db.vectors) == 2


@pytest.mark.asyncio
async def test_search_empty_database():
    db = VectorDB()

    query_vector = [1, 2, 3]
    results = await db.search(query_vector)

    assert results == []


@pytest.mark.asyncio
async def test_search_basic():
    db = VectorDB()

    db.add_vector([1, 0, 0], "x-axis")
    db.add_vector([0, 1, 0], "y-axis")
    db.add_vector([0, 0, 1], "z-axis")
    db.add_vector([1, 1, 0], "diagonal")

    query_vector = [1, 0, 0]
    results = await db.search(query_vector, top_k=2)

    assert len(results) == 2

    metadata = ["x-axis", "y-axis", "z-axis", "diagonal"]
    for similarity, meta in results:
        assert isinstance(similarity, float)
        assert meta in metadata


@pytest.mark.asyncio
async def test_search_top_k_limit():
    db = VectorDB()

    db.add_vector([1, 0], "pos_x")
    db.add_vector([0, 1], "pos_y")
    db.add_vector([-1, 0], "neg_x")
    db.add_vector([0, -1], "neg_y")
    db.add_vector([1, 1], "diagonal")

    query_vector = [1, 0]

    results = await db.search(query_vector, top_k=1)
    assert len(results) == 1

    results = await db.search(query_vector, top_k=3)
    assert len(results) == 3

    results = await db.search(query_vector, top_k=10)
    assert len(results) == 5


@pytest.mark.asyncio
async def test_search_default_top_k():
    db = VectorDB()

    for i in range(7):
        db.add_vector([i + 1, 1], f"vec_{i}")

    query_vector = [1, 0]
    results = await db.search(query_vector)

    assert len(results) == 5


@pytest.mark.asyncio
async def test_search_single_vector():
    db = VectorDB()

    db.add_vector([1, 2, 3], "single_doc")

    query_vector = [1, 2, 3]
    results = await db.search(query_vector, top_k=5)

    assert len(results) == 1
    similarity, meta = results[0]
    assert abs(similarity - 1.0) < 1e-10
    assert meta == "single_doc"


@pytest.mark.asyncio
async def test_full_workflow():
    db = VectorDB()

    db.add_vector([1, 0, 0], "doc1")
    db.add_vector([0, 1, 0], "doc2")
    db.add_vector([0, 0, 1], "doc3")
    db.add_vector([1, 1, 1], "doc4")

    assert len(db.vectors) == 4
    assert len(db.metadata) == 4
    assert db.vector_dim == 3

    query_vector = [1, 0, 0]
    results = await db.search(query_vector, top_k=2)

    assert len(results) == 2
    similarity, meta = results[0]
    assert abs(similarity - 1.0) < 1e-10
    assert meta == "doc1"
