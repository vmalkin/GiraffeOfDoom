def get_index(start, stop, current, length):
    i = (current - start) / (stop - start)
    i = int(i * length)
    return i

print(get_index(0, 2000, 1800, 700))
