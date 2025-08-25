# Deploy the vector DB on your own, and implement the `vector cosine similarity` without using a high level library.

## Approach

- Implement simple in-memory vector and metadata using list.
- Implement `vector cosine similarity` without using external libraries by defining simple dot product and vector length/magnitude method.
- Parallel search calculation by leveraging `to_thread` from `asyncio` to make sync function to run in async.

## Future Improvements

### HNSW (Hierarchical Navigable Small World)

Implement HNSW algorithm to reduce search complexity for faster result with some additional memory complexity.
