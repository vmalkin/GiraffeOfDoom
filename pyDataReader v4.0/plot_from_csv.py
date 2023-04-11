import mgr_plot_diurnal
import mgr_plot_diffs
import mgr_emd
import mgr_plot_detrended
import constants as k

station_id = k.station_id
database = k.database
logfile_dir = k.logfile_dir
publish_dir = k.publish_dir
filename = "data.csv"

mgr_plot_diurnal.wrapper(filename, publish_dir)
mgr_plot_diffs.wrapper(filename, publish_dir)
mgr_plot_detrended.wrapper(filename, publish_dir)
mgr_emd.wrapper(filename, publish_dir)
