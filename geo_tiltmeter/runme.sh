#!/bin/bash
display_menu() {
  clear
  echo ""
  echo "PENDULUM VISUALISATION"
  echo "~~~~~~~~~~~~~~~~~~~~~~"
  echo ""
  echo "Are we running in VENV? Is the datalogger running?"
  echo "Choose from the following menu."
  echo "Check the status of the datalogger first."
  echo ""
  echo "[b] Basic spectrogram and 24 hour readings."
  echo "[f] FFT of last 24 hours."
  echo "[s] Statistical analysis."
  echo ""
  echo "[q] QUIT the program."
  echo ""
  }


user_q() {
  echo "QUIT program"
  global_run=0
}


user_b() {
  echo "Basic spectrogram."
  python3 master_plotter.py
}


user_f() {
  echo "FFT spectrograms via multi-processing."
  python3 multiprc_fft.py
}


user_s() {
  echo "Statistical analysis of data for 24 hours."
  python3 master_statistics.py
}


check_user_input() {
  case $user_input in
  q)
    user_q
    ;;
  b)
    user_b
    ;;
  f)
    user_f
    ;;
  s)
    user_s
    ;;
  *)
    echo "Not valid input!"
    ;;
  esac
}


# ====== PROGRAM STARTS HERE =====
clear
global_run=1
source venv/bin/activate

while [ "$global_run" -eq 1 ];
do
  display_menu
  read -p "Choose an option." user_input
  check_user_input
  read -p "Press ENTER to continue..."
  done
