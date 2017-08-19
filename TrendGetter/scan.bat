#!/bin/bash

dir 2*.csv /b > files.txt

python trendGetter_3.py

pause