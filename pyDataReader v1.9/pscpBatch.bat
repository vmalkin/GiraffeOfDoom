color 75
ECHO OFF
rem PSCP batch script to send updated files to the server. For windows 7+
rem ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
rem 
rem We're going to use the Archive bit of the file to determine of it has been updated recently
rem if so, we will upload and reset the bit to -A
rem
rem We also need the pscp.exe utility

rem Set password string
SET server_pwd="neworion"

rem This code will run in a continuous loop
: runscp

REM Upload file fragment for each file
date /t
time /t
set uploadfile="C:\Users\Meepo\Desktop\pyDataReader v1.9\graphing\diffs.csv"
IF EXIST %uploadfile% PSCP -v -pw %server_pwd% %uploadfile% vmalkin@192.168.1.4:/home/vmalkin
rem del %uploadfile%
set uploadfile=""

TIMEOUT 15
REM GOTO runscp

:end
