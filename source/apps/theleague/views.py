import datetime

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404

from app_utils.tools import render_response
from apps.theleague.models import League, Match, Round, Season, Team


def scoreboard(request):
    """ Display the scoreboard
    """
    today = datetime.datetime.today()
    league = League.objects.get(pk=settings.LEAGUE_ID)
    divisions = league.division_set.all()
    rounds = Round.objects.filter(go_dead_date__lte=today).order_by('-go_live_date')

    # Is this the best way?  Maybe baby.
    first_division_rounds = []
    for r in rounds:
      first_division_rounds.append(divisions[0].match_set.filter(round=r))

    second_division_rounds = []
    for r in rounds:
      second_division_rounds.append(divisions[1].match_set.filter(round=r))

    return render_response(request, 'theleague/scoreboard.html', {
        'rounds': rounds,
        'first_division_rounds': first_division_rounds,
        'second_division_rounds': second_division_rounds,
    })


def schedule(request):
    """ Display the schedule
    """
    today = datetime.date.today()
    league = League.objects.get(pk=settings.LEAGUE_ID)
    seasons = league.current_seasons()
    divisions = league.division_set.all()

    # set up our weeks
    #seasons = []
    #for season in league.current_seasons():
        #rounds = []
        #matches = season.match_set.order_by('date')
        #prev_date = None
        #for match in matches:
            #if match.date != prev_date:
                #prev_date = match.date
                #rounds.append({
                    #'date': prev_date,
                    #'in_past': match.in_past,
                    #'matches': [],
                #})
            #rounds[-1]['matches'].append(match)
        #seasons.append({'season': season, 'rounds': rounds})

    return render_response(request, 'theleague/schedule.html', {
        'current_seasons': seasons,
        'divisions': divisions,
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


