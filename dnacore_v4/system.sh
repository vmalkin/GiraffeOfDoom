#!/bin/bash
while :
do
 python3.5 get_ruru.py
 python3.5 get_goes16.py
 python3.5 get_SW_speed.py
 python3.5 get_SW_density.py
 python3.5 get_bz.py
 
 python3.5 save_logfiles.py
 python3.5 chart_dxdt.py
 python3.5 chart_bz.py
 python3.5 chart_goes.py
 python3.5 chart_ruru.py
 
 echo " "
 echo "Processing completed for this cycle. Waiting 300 seconds... "
 echo " "
 sleep 300
done
