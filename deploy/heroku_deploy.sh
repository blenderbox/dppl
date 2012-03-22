#!/bin/bash

# Bash colors
BOLD="$(tput bold)"
RESET="$(tput sgr0)"
RED="$(tput setaf 1)"
YELLOW="$(tput setaf 3)"
GREEN="$(tput setaf 2)"

# Binaries
GIT=$(which git)
PYTHON=$(which python)
MANAGE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../source/manage.py"

function handle_error {
  echo -e "\n${1}\t\t\t${RED}${BOLD}[Failed]${RESET}"
  exit 1
}

fail=0

$PYTHON $MANAGE collectstatic --noinput --ignore="public/CACHE/*" || fail=1
if [ $fail -eq 1 ]; then
  handle_error "Collect Static"
fi

$PYTHON $MANAGE compress || fail=1
if [ $fail -eq 1 ]; then
  handle_error "Compressor"
fi

$GIT push heroku master || fail=1
if [ $fail -eq 1 ]; then
  handle_error "Heroku"
fi

# Everything worked!
echo -e "\n${BOLD}${GREEN}Deployed to Heroku, remember to run migrations manually!${RESET}"
