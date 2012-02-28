import sys

from source.settings.defaults import *


DEBUG = True
LOCAL_SERVE = True
TEMPLATE_DEBUG = True

# To run a testing server:
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

if len(set(sys.argv) & set(('test', 'zen'))) > 0:
    # Running tests, so just use a sqlite db
    DATABASES = {
        'default': {
            'ENGINE': "django.db.backends.sqlite3",
            'NAME': "test.db",
        },
    }
else:
    # Real database when not testing
    DATABASES = {
        # 'default': {
        #     'ENGINE': "django.db.backends.mysql",
        #     'NAME': "dppl",
        #     'USER': "root",
        #     'PASSWORD': "root",
        # },
        'default': {
            'ENGINE': "django.db.backends.postgresql_psycopg2",
            'NAME': "dppl",
            'USER': "postgres",
            'PASSWORD': "postgres",
        },
    }

# Dummy cache for dev
CACHES = {
    'default': {
        'BACKEND': "django.core.cache.backends.dummy.DummyCache",
    },
}

# DB backed sessions for testing since cache dumps itself
SESSION_ENGINE = "django.contrib.sessions.backends.db"
