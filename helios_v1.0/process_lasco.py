import mgr_analyser_v2
import mgr_enhancer_v2
import global_config
import time
import os

enhanced_folder = global_config.folder_source_images + os.sep + "enhanced_lasco"
storage_folder = global_config.folder_source_images + os.sep + "store_lasco_512"
analysis_folder = global_config.folder_source_images + os.sep + "analysis_lasco"
processing_start_date = int(time.time() - (86400 * 7))

if os.path.exists(enhanced_folder) is False:
    os.makedirs(enhanced_folder)
if os.path.exists(analysis_folder) is False:
    os.makedirs(analysis_folder)

mgr_enhancer_v2.wrapper(processing_start_date, storage_folder, enhanced_folder)
mgr_analyser_v2.wrapper(processing_start_date, storage_folder, analysis_folder)