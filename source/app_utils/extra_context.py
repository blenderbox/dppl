import datetime
from operator import itemgetter

from django.conf import settings
# from django.core.cache import cache
# from django.core.urlresolvers import reverse
from django.db.models import Sum

from apps.accounts.models import Profile
from apps.theleague.models import League, Team


def elo_rankings(request):
    """ This is used by the rankings widgets. """
    return {
        'PLAYERS': Profile.objects.filter(
            include_in_team=True).order_by('-exposure'),
    }


def extra_context(request):
    """ This provides some extra context for the templates. """
    we_live_yo = False
    today = datetime.date.today()
    league = League.objects.get(pk=settings.LEAGUE_ID)
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


def scoreboard(request):
    """ Display the scoreboard """
    today = datetime.datetime.today()
    league = League.objects.get(pk=settings.LEAGUE_ID)
    season = league.current_season

    if season is None:
        return {
            'FIRST_DIVISION_MATCHES': [],
            'SECOND_DIVISION_MATCHES': [],
        }

    divisions = league.division_set.all()
    rounds = season.round_set.filter(go_dead_date__lte=today)\
                .order_by('-go_live_date')[:1]

    first_division_matches = []
    second_division_matches = []

    if len(rounds) > 0:
        r = rounds[0]
        # We're assuming there are two divisions
        first_division_matches = divisions[0].match_set.filter(round=r)
        second_division_matches = divisions[1].match_set.filter(round=r)

    return {
        'FIRST_DIVISION_MATCHES': first_division_matches,
        'SECOND_DIVISION_MATCHES': second_division_matches,
    }


def standings(request):
    """ Display the standings
        TODO: cache this bad boy.
    """
    league = League.objects.get(pk=settings.LEAGUE_ID)
    season = league.current_season
    division_standings = []
    add = lambda x, y: (x or 0) + (y or 0)

    if season is None:
        return {'STANDINGS': division_standings}

    divisions = league.division_set.all()

    for division in divisions:
        team_standings = []
        for team in division.team_set.all():
            s1 = team.team1.aggregate(wins=Sum('team1_score'),
                                      losses=Sum('team2_score'))
            s2 = team.team2.aggregate(wins=Sum('team2_score'),
                                      losses=Sum('team1_score'))

            wins = add(s1['wins'], s2['wins'])
            losses = add(s1['losses'], s2['losses'])
            total = wins + losses
            percent = (float(wins) / total) * 100 if total > 0 else 0

            team_standings.append({
                    'team': team,
                    'wins': wins,
                    'losses': losses,
                    'percent': "%.0f" % percent,
                    })
        team_standings.sort(key=itemgetter('wins'), reverse=True)
        division_standings.append({
            'division': division,
            'standings': team_standings,
            })

    return {'STANDINGS': division_standings}


def team_nav(request):
    """ Set the teams in the app.
        TODO: Cache this?
    """
    teams = Team.objects.all()

    return {'TEAMS': teams}
