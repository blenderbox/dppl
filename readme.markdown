# Local Development
1.  Check out the repo:

        $ git clone git://github.com/blenderbox/dppl.git

1.  Create a virtual environment:

        $ mkvirtualenv dppl --no-site-packages

1.  Enter your vitrtual environment, and install the packages:

        $ workon dppl
        $ easy_install pip
        $ pip install -r requirements.txt

1.  Copy settings/local.py.example to local.py, and customize with your
    database info:

        $ cp source/settings/local.py.example source/settings/local.py

1.  Create your database, then run syncdb and fake migrations:

        $ python source/manage.py syncdb --all
        $ python source/manage.py migrate --fake

1.  Startup your server:

        $ python source/manage.py runserver


# Heroku
1.  The Heroku server is (currently) located at: http://dppl.herokuapp.com

1.  Email djablons at blenderbox dot com to get access as a developer.

1.  Install the Heroku package, and signup: http://devcenter.heroku.com/articles/quickstart

1.  Once you've gained access, you can run any basic commands using:

        $ heroku run "python source/manage.py <some command> --settings=source.settings.heroku"

1.  To deploy, just run:

        $ git push heroku master


## Note
This article will definitely be helpful for Heroku stuff:
http://devcenter.heroku.com/articles/quickstart

This one will be helpful if you're adding your own settings:
http://rdegges.com/devops-django-part-3-the-heroku-way

If you're starting a new Heroku server, you'll need to set up some
environment variables in order to get it working. To set up an
environment variable, you must run:

    $ heroku config:add MY_VARIABLE="my_value"

Here are the environment variables you'll need to add:

*   **AWS_ACCESS_KEY_ID**: Your AWS access id for S3 storage.

*   **AWS_SECRET_ACCESS_KEY**: Your AWS secret key for S3 storage.

*   **AWS_STORAGE_BUCKET_NAME**: The S3 bucket name you put the files
    in.

*   **DJANGO_SETTINGS_MODULE**: This should probably be `source.settings.heroku`
    unless you use a different settings file.

Once you've pushed to Heroku, you'll have to remotely run syncdb, and
collect static. To do this:

    $ heroku run "python source/manage.py syncdb --all --noinput --settings=source.settings.heroku"
    $ heroku run "python source/manage.py collectstatic --noinput --settings=source.settings.heroku"
    $ heroku run "python source/manage.py createsuperuser --settings=source.settings.heroku"
