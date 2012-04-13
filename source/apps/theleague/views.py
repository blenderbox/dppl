import datetime
from itertools import groupby

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from app_utils.tools import render_response
from apps.accounts.models import Profile
from apps.theleague.models import League, Team, Match


@cache_page(60 * 30)
def scoreboard(request):
    """ Display the scoreboard. """
    now = datetime.datetime.now()
    league = League.objects.get(pk=settings.LEAGUE_ID)
    season = league.current_season

    if season is None:
        return render_response(request, 'theleague/scoreboard.html', {
                  'rounds': None,
                  'first_division_rounds': [],
                  'second_division_rounds': [],
              })

    divisions = league.division_set.all()
    rounds = season.round_set.select_related().filter(
            go_dead_date__lt=now).order_by('-go_live_date')

    # All of the round ids as a list
    round_ids = [r.id for r in rounds]

    # A lambda to get matches by division
    matches = lambda i: Match.objects.filter(
            division__id=divisions[i].id, round__id__in=round_ids)

    # A lambda to regroup the matches by round
    division = lambda x: [(k, list(g)) for k, g in groupby(
                    matches(x),
                    key=lambda o: getattr(o, 'round'),
                )]

    return render_response(request, 'theleague/scoreboard.html', {
        'rounds': rounds,
        # Get the round-grouped matches of the first division in `divisions`
        'first_division_rounds': division(0),
        # Get the round-grouped matches of the second division in `divisions`
        'second_division_rounds': division(1),
    })


def schedule(request):
    """ Display the schedule """
    league = League.objects.get(pk=settings.LEAGUE_ID)
    seasons = league.current_seasons()
    divisions = league.division_set.all()

    return render_response(request, 'theleague/schedule.html', {
        'current_seasons': seasons,
        'divisions': divisions,
    })


def team(request, team_slug=None):
    """ Display the team. """
    league = League.objects.get(pk=settings.LEAGUE_ID)
    objs = Team.objects.filter(division__league__id=settings.LEAGUE_ID)

    if team_slug is not None:
        objs = objs.filter(slug=team_slug)

    try:
        team = objs[:1][0]
    except IndexError:
        raise Http404

    return render_response(request, 'theleague/team.html', {
        'schedule': team.current_schedule(league.current_season),
        'team': team,
    })


def team_member(request, team_slug, team_member_slug):
    """ Display the team """
    league = League.objects.get(pk=settings.LEAGUE_ID)
    # TODO: make this actually pull in teams just from the league.
    team = get_object_or_404(Team, slug=team_slug)

    try:
        profile = team.profile_team.get(slug=team_member_slug)
    except Profile.DoesNotExist:
        raise Http404

    return render_response(request, 'theleague/team_member.html', {
        'schedule': team.current_schedule(league.current_season),
        'team': team,
        'profile': profile,
    })
