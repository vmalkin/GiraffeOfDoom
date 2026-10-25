import multiprc_fft
import time


start = time.time()

multiprc_fft.main()

# =========================================================
# Some stats on processing time.
end = time.time()
elapsed_time = end - start
print(f"\n")
print(f"Elapsed time: {elapsed_time / 60:.2f} minutes.")
print(f'\n*** END Plotter ***')