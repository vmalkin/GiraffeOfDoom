import mgr_binner
import mgr_data


mag_read_freq = 30   # how many readings per minute
mag_running_count = 6   # width of the window for running average
noise_spike = 2   # threshold for rate of change noise
field_correction = -1   # graph should go up, as H value increases
station_id = "Ruru_Rapid"   # ID of magnetometer station


d_mg = mgr_data.DataList()
binner = mgr_binner.Binner(d_mg.data_array, 86400, 60, field_correction)

binner.processbins()