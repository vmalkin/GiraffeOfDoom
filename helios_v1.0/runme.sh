#!/usr/bin/env bash
venv/bin/python download_lasco.py
venv/bin/python download_suvi.py

venv/bin/python process_suvi_diffs.py
venv/bin/python process_mlti_clr_suvi.py
