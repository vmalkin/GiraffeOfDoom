#!/bin/bash
while :
do
 python3 kindex.py
 python3 station_Bz.py
 python3 station_GIC.py
 python3 station_GOES.py
 python3 station_rururapid.py
 python3 station_solarwind.py
 echo " "
 echo "Processing completed for this cycle. Waiting 300 seconds... "
 echo " "
 sleep 300
done
