# Explain how it's different from splitting the small vs large files.

In the small file case I'm not exactly splitting the files but instead load the file directly into memory.

Meanwhile for the larger file case, the main idea is to not exactly do what I did with the small file.
The idea is to load small part of the data one at a time into the memory, the advantage is lower resource yes but it also means we need to slightly change our way of processing the data as we need a some kind of placeholder to get the insight we want from the small chunk and globaly merge them afterwards.
