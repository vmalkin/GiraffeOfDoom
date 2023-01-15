import mgr_plot_diffs
import constants as k

print("*** dhdt: Start")
# unprocessed magnetogram/data
mgr_plot_diffs.wrapper(k.database, k.publish_dir)
print("*** dhdt: Finish")
