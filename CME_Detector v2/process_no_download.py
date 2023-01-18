import mgr_analyser_v2
import mgr_enhancer_v2

enhanced_folder = "enhanced_512"
storage_folder = "lasco_store_512"
analysis_folder = "analysis_512"

mgr_enhancer_v2.wrapper(storage_folder, enhanced_folder)
mgr_analyser_v2.wrapper(enhanced_folder, analysis_folder)