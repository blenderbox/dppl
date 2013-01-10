# -*- coding: utf-8 -*-
# vim: ft=python
import os


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
DEBUG = False

TEMPLATE_DEBUG = DEBUG

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

SECRET_KEY = ''

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
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',

    # Project Context Processors
    'source.app_utils.extra_context.elo_rankings',
    'source.app_utils.extra_context.extra_context',
    'source.app_utils.extra_context.scoreboard',
    'source.app_utils.extra_context.standings',
    'source.app_utils.extra_context.team_nav',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

if USE_I18N:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

ROOT_URLCONF = 'source.urls'

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

WSGI_APPLICATION = 'source.wsgi.application'


#############
# DATABASES #
#############

DATABASES = {
    'default': {},
}


#########
# PATHS #
#########

def get_path(*args):
    return os.path.realpath(os.path.join(*args))

PROJECT_DIR = get_path(os.path.dirname(__file__), "../")

LOG_ROOT = get_path(PROJECT_DIR, '../logs')

MEDIA_URL = '/media/'
MEDIA_ROOT = get_path(PROJECT_DIR, '../media/')

STATIC_URL = '/static/'
STATIC_ROOT = get_path(PROJECT_DIR, '../static/')

STATICFILES_DIRS = (
    get_path(PROJECT_DIR, '../public/'),
)

TEMPLATE_DIRS = (
    get_path(PROJECT_DIR, 'templates'),
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


################
# APPLICATIONS #
################

PROJECT_APPS = (
    'source.app_utils.bootstrap',
    'source.apps.accounts',
    'source.apps.pages',
    'source.apps.theleague',
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
    'source.templatetags.helper_tags',
    'source.templatetags.verbatim',
)

AUTHENTICATION_BACKENDS = (
    # For allowing email addresses as usernames. Must come before django stuff
    'source.apps.accounts.backends.EmailBackend',
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
