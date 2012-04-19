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

function static {
    $PYTHON $MANAGE collectstatic --noinput --ignore="public/CACHE/*"
    $PYTHON $MANAGE compress
}

function deploy {
    $GIT push heroku master
}

function warn {
    echo -e "\n${BOLD}${YELLOW}${1}${RESET}"
}

function success {
    echo -e "\n${BOLD}${GREEN}${1}${SUCCESS}"
}

if [ "${1}" == "--static" ]; then
    warn "Collecting Static, and Compressing\n---"
    static

elif [ "${1}" == "--deploy" ]; then
    warn "Deploying\n---"
    deploy

else
    warn "Collecting Static, Compressing, then Deploying\n---"
    static && deploy

fi

success "[ Complete ]"
