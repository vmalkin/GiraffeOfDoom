:start
rem Get basic data and plot the basic csv files
python get_ruru.py
python get_goes16.py
python get_SW_speed.py
python get_SW_density.py
python get_bz.py

rem Save basic CSV files. Logs for 24 hrs and the nowfiles for display
python save_logfiles.py
python chart_dxdt.py

REM Chart the Spark Plots for the front page
python chart_spark_bz.py
python chart_spark_ruru.py
python chart_spark_goes16.py

REM Special monitoring  for alerts


timeout 480
goto start