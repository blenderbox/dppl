"""
This allows you to run `$ python manage.py runserver` without specifying the
settings.
Just symlink source/settings/<file_name>.py to source/settings/local.py
"""
try:
    from source.settings.local import *
except ImportError:
    pass
