REM Keep this script running
: runscp
color 03
D:\1_WIN_BIN\winscp577\winscp.com /script=scp.scp
color 75
echo "Connection Failure, retry in:"
timeout 20
goto runscp

:end


