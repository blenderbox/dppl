#!/bin/bash

GIT=$(which git)
PYTHON=$(which python)
MANAGE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../source/manage.py"

$PYTHON $MANAGE collectstatic --noinput
$PYTHON $MANAGE compress
$GIT push heroku master
