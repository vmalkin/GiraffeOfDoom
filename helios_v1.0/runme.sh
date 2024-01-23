#!/usr/bin/env bash

while [ true ]; do
  venv/bin/python download_lasco.py
  venv/bin/python process_lasco.py

  venv/bin/python download_suvi.py
  venv/bin/python process_suvi_diffs.py
  venv/bin/python process_mlti_clr_suvi.py
  venv/bin/python process_movies.py
  venv/bin/python process_histogram_analysis.py

  sleep 1h
done