:start
rem Get basic data and plot the basic csv files
python get_ruru.py
python get_goes16.py
python get_SW_speed.py
python get_SW_density.py
python get_bz.py
python plot_bins.py

rem specialised plotting files.
python plot_dxdt_v3.py

timeout 300
goto start