#!/bin/bash
# Text formatting
RESET='\033[0m'
BOLD='\033[1m'

# Colours
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
MAGENTA='\033[35m'
CYAN='\033[36m'
WHITE='\033[37m'


display_menu() {
  clear
  echo ""
  echo -e "${RED}${BOLD}TILT METER VISUALISATION"
  echo -e "~~~~~~~~~~~~~~~~~~~~~~~~${RESET}"
  echo -e "${GREEN}"
  echo "Are we running in VENV? Is the datalogger running?"
  echo "Choose from the following menu."
  echo "Check the status of the datalogger first."
  echo -e "${RESET}"
  echo "[b] Basic seismic spectrogram and 24 hour readings."
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
  echo ""
  python3 master_plotter.py
}


user_f() {
  echo "FFT spectrograms via multi-processing."
  echo ""
  python3 multiprc_fft.py
}


user_s() {
  echo "Statistical analysis of data for 24 hours."
  echo ""
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
  echo -e "${GREEN}"
  read -p "Choose an option: " user_input
  check_user_input
  read -p "Press ENTER to continue..."
  echo -e "${RESET}"
  done
