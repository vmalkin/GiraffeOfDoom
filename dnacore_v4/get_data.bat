:start
rem Get basic data and plot the basic csv files
python get_ruru.py
python get_goes16.py

rem python get_SW_speed.py
rem python get_SW_density.py
rem python get_bz.py

rem specialised plotting files.
python save_logfiles.py

rem python chart_dxdt.py
rem python chart_spark_bz.py
python chart_spark_goes.py
python chart_spark_ruru.py


timeout 300
goto start