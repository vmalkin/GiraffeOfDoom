#!/bin/bash
while :
do
 # Update internal database from main sources online
 python3 get_ruru.py
 python3 get_goes_primary.py
 python3 get_goes_secondary.py
 python3 get_solarwind.py

 # Process the spark graphs for home page
 python3 chart_spark_goes_secondary.py
 python3 chart_spark_goes_primary.py
 python3 chart_spark_ruru.py
 python3 chart_spark_swspeed.py
 python3 chart_spark_swdens.py
 python3 chart_spark_bz.py
 python3 DashboardManager.py

 # process data for Hi-res magnetographs for inside pages
 # python3 chart_dxdt.py


 echo " "
 echo "Processing completed for this cycle. Waiting 300 seconds... "
 echo " "
 sleep 300
done
