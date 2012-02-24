from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse

from apps.theleague.models import Team


def extra_context(request):
    """
    This provides some extra context for the templates.
    """
    return {
        'FILER_URL': settings.FILER_URL,
    }

def team_nav(request):
    """ Set the teams in the app.
        TODO: Cache this?
    """
    teams = Team.objects.all()
    # TODO: set the logic for whether the season is live or not.
    we_live_yo = True
    return {
        'TEAMS': teams,
        'we_live_yo': we_live_yo,
    }
