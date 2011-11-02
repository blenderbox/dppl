import os

def path(*args):
    """ Get the full path of any joined path. """
    return os.path.realpath(os.path.join(*args))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Damon Jablons', 'djablons@blenderbox.com'),
    ('Nick Herro', 'nherro@blenderbox.com'),
    ('Brett Berman', 'bberman@blenderbox.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # 'postgresql_psycopg2', 'mysql', 'sqlite3'.
        'NAME': '', # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Internationalization machinery
USE_I18N = False
USE_L10N = False

# This dynamically discovers the path to the project
PROJECT_PATH = path(os.path.dirname(__file__))

MEDIA_ROOT = path(PROJECT_PATH, '../media')
MEDIA_URL = '/media/'
STATIC_ROOT = path(PROJECT_PATH, '../statique')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '%sadmin/' % STATIC_URL

STATICFILES_DIRS = (
    path(PROJECT_PATH, '../static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'finders.AppMediaDirectoriesFinder',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'localdev'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

# Context Processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

if USE_I18N:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = ()
for root, dirs, files in os.walk(PROJECT_PATH):
    if 'templates' in dirs: TEMPLATE_DIRS += (path(root, 'templates'),)

# Keeping these seperate for running tests
PROJECT_APPS = (

)

INSTALLED_APPS = (
    # Django Applications
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Django Applications
    'django_extensions',
) + PROJECT_APPS

TEMPLATE_TAGS = (
    # 'put.some.templatetags.here',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from local_settings import *
except ImportError:
    print "Could not find local_settings.py, nice one bro."
