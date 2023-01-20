import mgr_analyser_v2
import mgr_enhancer_v2
import time
import os

enhanced_folder = "enhanced_512"
storage_folder = "lasco_store_512"
analysis_folder = "analysis_512"
processing_start_date = int(time.time() - (86400 * 7))

if os.path.exists(enhanced_folder) is False:
    os.makedirs(enhanced_folder)
if os.path.exists(storage_folder) is False:
    os.makedirs(storage_folder)
if os.path.exists(analysis_folder) is False:
    os.makedirs(analysis_folder)

mgr_enhancer_v2.wrapper(processing_start_date, storage_folder, enhanced_folder)
mgr_analyser_v2.wrapper(processing_start_date, storage_folder, analysis_folder)