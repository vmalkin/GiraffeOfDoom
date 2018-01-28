#!/bin/bash

dir 2*.csv /b > files.txt

python ch_plotter.py

pause