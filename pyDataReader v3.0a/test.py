import mgr_grapher
import mgr_data
import mgr_files
import constants as k

filemanager = mgr_files.FileManager()
datamanager = mgr_data.DataList()

templist = mgr_grapher.median_window_filter(datamanager.data_array, 20)
templist = mgr_grapher.recursive_filter(templist)

binlist = mgr_grapher.BinBinlist(60, templist, k.publish_folder + "/dna_ppm1.csv")
binlist.process_datalist()
binlist.save_file()
