#!/bin/bash
while :
do
 python3 get_ruru.py
 python3 get_goes16.py
 python3 get_goes17.py
 python3 get_SW_speed.py
 python3 get_SW_density.py
 python3 get_bz.py
 python3 get_VLF.py
 
 python3 save_logfiles.py
 python3 chart_dxdt.py
 
 python3 chart_spark_bz.py
 python3 chart_spark_goes16.py
 python3 chart_spark_goes17.py
 python3 chart_spark_ruru.py
 python3 chart_spark_swspeed.py
 python3 chart_spark_swdens.py
 
 python3 DashboardManager.py
 
 echo " "
 echo "Processing completed for this cycle. Waiting 300 seconds... "
 echo " "
 sleep 300
done
