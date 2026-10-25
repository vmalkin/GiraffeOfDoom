# This template uses multiprocessing to iterate over very large arrays of data. We will use the
# ProcessPoolExecutor as it's considered the more modern method.
# Yes - AI has helped me with the ideas, but as you can tell by the janky code, that bit is mine.
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
import class_aggregator
import constants as k


# There may be other functions here called by process_chunk


def process_chunk(chunk):
    # This is a _Worker_ which typically uses the chunk to process then generate a
    # single plot from this chunk. Return the filename of the plot.
    # Data is in form [posix, data1, data2, etc]. use aggregator to separate out.
    if chunk is None:
        return "No data to process for this chunk"
    else:
        fftdata = class_aggregator.aggregate_data(windowsize=1, querydata=chunk)
        utctimes = fftdata[0]
        data = fftdata[1]

        return filename


def chunks(data, chunkstep, chunklength):
    # In Python, yield turns a normal function into a generator so
    # it can produce values one at a time instead of returning everything at once.
    # Each time the generator runs up to a yield, it pauses and gives the value to
    # the caller, then continues later from where it left off. THis memory efficient
    for i in range(len(data), 0, -1 * chunkstep):
        if i - chunklength > 0:
            slicestart = i - chunklength
            sliceend = i
            seismo_data = data[slicestart:sliceend]
            yield seismo_data
        else:
            yield None


def wrapper(data):
    # each entry in data is [posix, data1, data2, etc].
    # The size of the FFT data we want to process (6 hours)
    chunklength = (k.datapersecond * 60) * 60 * 6
    # The next step we're picking the data off from. (Every 5 mins usually)
    chunkstep = (k.datapersecond * 60) * 5
    cores = cpu_count() - 1
    with ProcessPoolExecutor(max_workers=cores) as executor:
        results = list(
            executor.map(
                process_chunk,
                chunks(data, chunkstep, chunklength)
                )
            )
        return results