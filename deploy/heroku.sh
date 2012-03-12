#!/bin/bash

cd ../source/
python manage.py collectstatic --noinput
python manage.py compress
git push heroku master
