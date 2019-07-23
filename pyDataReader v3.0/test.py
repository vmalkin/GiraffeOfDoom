import mgr_grapher
import mgr_data
import mgr_files
import constants as k

filemanager = mgr_files.FileManager()
datamanager = mgr_data.DataList()

templist = mgr_grapher.deblip(datamanager.data_array)
binlist = mgr_grapher.BinBinlist(2, templist, k.publish_folder + "/dna_fgm1.csv")
binlist.process_datalist()
binlist.save_file()
