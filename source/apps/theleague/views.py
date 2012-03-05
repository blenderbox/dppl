import datetime

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404

from app_utils.tools import render_response
from apps.theleague.models import League, Team, Season, Match


def scoreboard(request):
    """ Display the scoreboard
    """
    today = datetime.date.today()
    league = League.objects.get(pk=settings.LEAGUE_ID)

    return render_response(request, 'theleague/scoreboard.html', {})


def schedule(request):
    """ Display the schedule
    """
    today = datetime.date.today()
    league = League.objects.get(pk=settings.LEAGUE_ID)

    # set up our weeks
    current_seasons = []
    for season in Season.current_seasons():
        dates = []
        matches = season.match_set.order_by('date')
        prev_date = None
        for match in matches:
            if match.date != prev_date:
                prev_date = match.date
                dates.append({
                    'date': prev_date,
                    'matches': [],
                })
            dates[-1]['matches'].append(match)
        current_seasons.append({'season': season, 'dates': dates})

    return render_response(request, 'theleague/schedule.html', {
        'current_seasons': current_seasons,
    })


def teams(request):
    """ Display the teams landing page
        TODO: Combine this with the team view.  This seems unnecessary.
    """
    league = League.objects.get(pk=settings.LEAGUE_ID)
    # TODO: make this actually pull in teams just from the league.
    teams = Team.objects.all()
    team = teams[0] if len(teams) > 0 else None

    return render_response(request, 'theleague/teams.html', {
        'teams': teams,
        'team': team,
    })


def team(request, team_slug):
    """ Display the team
    """
    league = League.objects.get(pk=settings.LEAGUE_ID)
    # TODO: make this actually pull in teams just from the league.
    teams = Team.objects.all()
    team = get_object_or_404(Team, slug=team_slug)

    return render_response(request, 'theleague/team.html', {
        'teams': teams,
        'team': team,
    })

def team_member(request, team_slug, team_member_slug):
    """ Display the team
    """
    league = League.objects.get(pk=settings.LEAGUE_ID)
    # TODO: make this actually pull in teams just from the league.
    teams = Team.objects.all()
    team = get_object_or_404(Team, slug=team_slug)

    try:
        team_member = team.profile_team.get(slug=team_member_slug)
    except Poll.DoesNotExist:
        raise Http404

    return render_response(request, 'theleague/team_member.html', {
        'teams': teams,
        'team': team,
        'team_member': team_member,
    })


