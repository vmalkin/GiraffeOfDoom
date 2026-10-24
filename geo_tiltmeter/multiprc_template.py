# This template uses multiprocessing to iterate over very large arrays of data. We will use the
# ProcessPoolExecutor as it's considered the more modern method.
# Yes - AI has helped me with the ideas, but as you can tell by the janky code, that bit is mine.
from concurrent.futures import ProcessPoolExecutor


# There may be other functions here called by process_chunk


def process_chunk(chunk):
    # This is a _Worker_ which typically uses the chunk to processing then generating a
    # single plot from this chunk. Return the filename of the plot.
    return filename


def chunks(data, size):
    # In Python, yield turns a normal function into a generator so
    # it can produce values one at a time instead of returning everything at once.
    # Each time the generator runs up to a yield, it pauses and gives the value to
    # the caller, then continues later from where it left off. THis memory efficient
    for i in range(0, len(data), size):
        yield data[i:i + size]


def wrapper(data):
    chunksize = 10000
    with ProcessPoolExecutor(max_workers=8) as executor:
        results = list(
            executor.map(
                process_chunk,
                chunks(data, chunksize)
        )
    )
    return results