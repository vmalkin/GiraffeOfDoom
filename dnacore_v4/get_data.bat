:start
rem Get basic data and plot the basic csv files
python get_ruru.py
python get_goes16.py
python get_SW_speed.py
python get_SW_density.py
python get_bz.py

rem specialised plotting files.
python save_logfiles.py
python chart_dxdt.py
python chart_bz.py
python chart_goes.py
python chart_ruru.py

timeout 300
goto start