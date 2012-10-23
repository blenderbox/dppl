import datetime
from functools import wraps
from operator import itemgetter

from django.conf import settings
from django.core.cache import cache
from django.db.models import Sum

from apps.accounts.models import Profile
from apps.theleague.models import Team, the_league


def cache_this(key):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            KEY_PREFIX = "context"
            cache_key = "%s:%s" % (KEY_PREFIX, key)
            data = cache.get(cache_key)
            if not data:
                data = func(*args, **kwargs)
                cache.set(cache_key, data, kwargs.get('timeout', 30 * 60))
            return data
        return inner
    return decorator


@cache_this("players_elo_rankings")
def elo_rankings(request):
    """ This is used by the rankings widgets. """
    return {
            'PLAYERS': Profile.objects.filter(
                include_in_team=True).order_by('-exposure'),
            }


@cache_this("default_extra_context")
def extra_context(request):
    """ This provides some extra context for the templates. """
    we_live_yo = False
    today = datetime.date.today()
    league = the_league(settings.LEAGUE_ID)
    season = league.season_set.exclude(go_live_date__gt=today)\
                .order_by('-go_live_date')[:1]

    if len(season) > 0:
        s = season[0]
        we_live_yo = s.go_live_date <= today and (
                s.go_dead_date is None or s.go_dead_date >= today)

    return {
            'FILER_URL': settings.FILER_URL,
            'WE_LIVE_YO': we_live_yo,
            }


@cache_this("the_scoreboard")
def scoreboard(request):
    """ Display the scoreboard. """
    today = datetime.datetime.today()
    league = the_league(settings.LEAGUE_ID)
    season = league.current_season
    matches = [[], []]

    if season:
        divisions = league.division_set.all()
        rounds = (season.round_set.filter(go_dead_date__lte=today)
                  .values_list('id', flat=True).order_by('-go_live_date')[:1])

        if rounds:
            matches[0] = divisions[0].match_set.filter(round=rounds[0])
            matches[1] = divisions[1].match_set.filter(round=rounds[0])

    return {
        'FIRST_DIVISION_MATCHES': matches[0],
        'SECOND_DIVISION_MATCHES': matches[1],
    }


@cache_this("the_standings")
def standings(request):
    """ Display the standings """
    season = the_league(settings.LEAGUE_ID).current_season
    return {'STANDINGS': season.get_standings() if season else []}


@cache_this("team_nav")
def team_nav(request):
    """ Set the teams in the app.  """
    return {'TEAMS': Team.objects.all()}
