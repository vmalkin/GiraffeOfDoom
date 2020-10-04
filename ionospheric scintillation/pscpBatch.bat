title Magneto Uploader
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
SET server_pwd="passwords suck arse"

rem This code will run in a continuous loop
: runscp

REM Upload file fragment for each file
date /t
time /t
set uploadfile="*.csv"
IF EXIST %uploadfile% PSCP -v -pw %server_pwd% %uploadfile% vaughn@dunedinaurora.nz:/var/www/html
rem del %uploadfile%
set uploadfile=""

TIMEOUT 600
GOTO runscp

:end
