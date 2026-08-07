#!/bin/bash
while :
do
 python3 get_ruru.py
 python3 get_goes_primary.py
 python3 get_goes_secondary.py
 python3 get_solarwind.py

 python3 chart_spark_goes_secondary.py
 python3 chart_spark_goes_primary.py
 python3 chart_spark_ruru.py

 python3 chart_spark_swspeed.py
 python3 chart_spark_swdens.py
# python3 chart_dxdt.py
 python3 chart_spark_bz.py
 python3 DashboardManager.py
 
 echo " "
 echo "Processing completed for this cycle. Waiting 300 seconds... "
 echo " "
 sleep 300
done
