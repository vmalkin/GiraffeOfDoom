#!/bin/bash
# MAIN.PY is the main script that will take mag data 
# and create logfiles.
# PUBLISHDATA.PY creates csv display files for charting
cd /home/vmalkin/Magnetometer/dalmoreP/pyDataReader
screen -S "Prime Main" -d -m python3 main.py
screen -S "Prime Publish Manager" -d -m python3 publishdata.py

# Runs the SCP uploading
screen -S "Prime Server Upload" -d -m bash scpBash.sh

# Ancilliary projects
cd /home/vmalkin/Magnetometer/dalmoreP/DataFusionProject
screen -S "Prime Datafusion" -d -m python3 main.py

cd /home/vmalkin/Magnetometer/dalmoreP/testSpike
screen -S "Prime Spikes" -d -m python3 main.py
