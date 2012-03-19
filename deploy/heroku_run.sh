#!/bin/bash

heroku run "python source/manage.py ${@} --settings=source.settings.heroku"
