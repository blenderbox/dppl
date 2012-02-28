from django.conf import settings
from django.template import add_to_builtins

""" This file will load anything in your settings.TEMPLATE_TAGS into Django's
template_tag library so that you can use them anywhere without explicitly
loading them. This makes things a bit DRYer.
"""

__path__ = ""

try:
    for lib in settings.TEMPLATE_TAGS:
        add_to_builtins(lib)
except AttributeError:
    pass
