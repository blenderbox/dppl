from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse


def extra_context(request):
    """
    This provides some extra context for the templates.
    """
    return {
        'FILER_URL': settings.FILER_URL,
    }
