#!/bin/bash

dir 2*.csv /b > files.txt

python kindexer.py

pause