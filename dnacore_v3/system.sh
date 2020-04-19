#!/bin/bash
while :
do
 python3 kindex.py
 python3 get_ruru.py
 python3 get_goes16.py
 python3 get_SW_speed.py
 python3 get_SW_density.py
 python3 get_bz.py
 
 python3 plot_bins.py
 python3 plot_detrended.py
 python3 plot_dxdt.py
 echo " "
 echo "Processing completed for this cycle. Waiting 300 seconds... "
 echo " "
 sleep 300
done
