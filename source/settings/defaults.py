# -*- coding: utf-8 -*-
import os
from sys import argv


gettext = lambda s: s


########################
# MAIN DJANGO SETTINGS #
########################

ADMINS = (
    ("Damon Jablons", 'djablons@blenderbox.com'),
    ("Nick Herro", 'nherro@blenderbox.com'),
    ("Brett Berman", 'bberman@blenderbox.com'),
    ("Caleb Brown", 'cbrown@blenderbox.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = [('en', 'English')]

DEFAULT_LANGUAGE = 0

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Set DEBUG = True if on the production server
LOCAL_SERVER_ARGS = (
    'runserver', 'runserver_plus', 'runprofileserver', 'shell', 'shell_plus',
)
if len(set(argv) & set(LOCAL_SERVER_ARGS)) > 0:
    DEBUG = True
else:
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#    'django.template.loaders.eggs.Loader',
#    'django.template.loaders.app_directories.load_template_source',
)

SECRET_KEY = 'localdev'

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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    # Project Context Processors
    'app_utils.extra_context.elo_rankings',
    'app_utils.extra_context.extra_context',
    'app_utils.extra_context.scoreboard',
    'app_utils.extra_context.standings',
    'app_utils.extra_context.team_nav',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

if USE_I18N:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

ROOT_URLCONF = 'urls'

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

#############
# DATABASES #
#############

DATABASES = {
    'default': {
        # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': '',
        # DB name or path to database file if using sqlite3.
        'NAME': '',
        # Not used with sqlite3.
        'USER': '',
        # Not used with sqlite3.
        'PASSWORD': '',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
         # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}


#########
# PATHS #
#########

def get_path(*args):
    return os.path.realpath(os.path.join(*args))

PROJECT_DIR = get_path(os.path.dirname(__file__), "../")

LOG_ROOT = get_path(PROJECT_DIR, '../logs')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = get_path(PROJECT_DIR, "../", MEDIA_URL.strip("/"))

STATIC_URL = '/static/'

STATIC_ROOT = get_path(PROJECT_DIR, "../", STATIC_URL.strip("/"))

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don"t forget to use absolute paths, not relative paths.
    get_path(PROJECT_DIR, "../public"),
)

TEMPLATE_DIRS = (
    get_path(PROJECT_DIR, "templates"),
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


################
# APPLICATIONS #
################

PROJECT_APPS = (
    'app_utils.bootstrap',
    'apps.accounts',
    'apps.pages',
    'apps.theleague',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',

    # Third Party Django Applications
    'compressor',
    'django_extensions',
    'easy_thumbnails',
    'filer',
    'gunicorn',
    'imagekit',
    'mptt',
    'south',
) + PROJECT_APPS

TEMPLATE_TAGS = (
    # Third Party
    'easy_thumbnails.templatetags.thumbnail',
    # Project
    'templatetags.helper_tags',
    'templatetags.verbatim',
)

AUTHENTICATION_BACKENDS = (
    # For allowing email addresses as usernames. Must come before django stuff
    'apps.accounts.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

########################
# APPLICATION SETTINGS #
########################

STATIC_REDIRECTS = [
    'apple-touch-icon.png', 'favicon.ico', 'humans.txt', 'robots.txt',
]

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)

FILER_URL = MEDIA_URL + 'filer_thumbnails/'

LEAGUE_ID = 1

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.filters',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
)
