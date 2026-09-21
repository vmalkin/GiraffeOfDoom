import mgr_database
import standard_stuff
import plotter_spectrum
import plotter_dual
import plotter_current_day
import plotter_fft_movie
import time
from datetime import datetime, timezone
import os
import constants as k
import numpy as np


if __name__ == "__main__":
    # assume time period is a day
    seconds_per_day = 86400
    elapsed_start = time.time()
    print(f"*** BEGIN plots.")
    end_time = time.time()
    start_time = end_time - seconds_per_day
    # data = mgr_database.db_data_get(start_time, end_time)
    data = mgr_database.db_data_all()
    print(f"*** Data downloaded from DB.")

    # Basic cleanup of data.
    # Matplotlib needs UTC time objects.
    # Remove None from data and remove corresponding time objects from UTC time.
    # We will allow the plotters to deal with gaps in data.
    data_tilt = []
    data_utc_objects = []
    for psx, tilt in data:
        if isinstance(tilt, float):
            data_tilt.append(tilt)
            tim = datetime.fromtimestamp(psx, tz=timezone.utc)  # datetime object
            data_utc_objects.append(tim)

    # Send data to the plotters
    # plotter_dual.wrapper(data_utc_objects, data_tilt)
    # plotter_current_day.wrapper(data_utc_objects, data_tilt)
    # plotter_spectrum.wrapper(data_utc_objects, data_tilt)
    plotter_fft_movie.wrapper(data_utc_objects, data_tilt)

    # Some stats on processing time.
    elapsed_end = time.time()
    elapsed_time = elapsed_end - elapsed_start
    print(f"\n")
    print(f"Readings per second: {len(data) / seconds_per_day}")
    print(f"Elapsed time: {elapsed_time / 60:.2f} minutes")
    print(f"*** All plots completed.")
