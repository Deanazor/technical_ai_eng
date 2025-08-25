# Please parse large CSV, customers-2000000.csv and keep the memory low.

There are 3 approach that I use in this case:

1. Using pandas with chunksize
2. Using polars lazy load
3. Vanilla csv reader and read them per-row
