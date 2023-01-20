import mgr_analyser_v2
import mgr_enhancer_v2
import time

enhanced_folder = "enhanced_512"
storage_folder = "lasco_store_512"
analysis_folder = "analysis_512"
processing_start_date = int(time.time() - (8640 * 7))

mgr_enhancer_v2.wrapper(processing_start_date, storage_folder, enhanced_folder)
mgr_analyser_v2.wrapper(processing_start_date, enhanced_folder, analysis_folder)