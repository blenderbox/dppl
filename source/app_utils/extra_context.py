import datetime

from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse

from apps.theleague.models import Season, Team


def extra_context(request):
    """
    This provides some extra context for the templates.
    """
    we_live_yo = False
    today = datetime.date.today()
    season = Season.objects.exclude(go_live_date__gt=today)\
                .order_by('-go_live_date')[:1]

    if len(season) > 0:
        s = season[0]
        we_live_yo = s.go_live_date <= today and (s.go_dead_date is None or s.go_dead_date >= today)
    
    return {
        'FILER_URL': settings.FILER_URL,
        'WE_LIVE_YO': we_live_yo,
    }


def team_nav(request):
    """ Set the teams in the app.
        TODO: Cache this?
    """
    teams = Team.objects.all()
    
    return {
        'TEAMS': teams,
    }
