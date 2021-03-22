:start
rem Get basic data and plot the basic csv files
python get_ruru.py
python get_goes16.py

REM python get_SW_speed.py
REM python get_SW_density.py
python get_bz.py

rem specialised plotting files.
python save_logfiles.py

python chart_dxdt.py
python chart_spark_bz.py
python chart_spark_ruru.py
python chart_spark_goes.py

timeout 480
goto start