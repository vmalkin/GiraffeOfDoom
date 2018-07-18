#!/bin/bash

dir 2*.csv /b > files.txt

python trendGetter_8.py

pause