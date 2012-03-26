import datetime
from itertools import groupby

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from app_utils.tools import render_response
from apps.theleague.models import League, Team, Match, Game


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
    """ Display the team
    """
    league = League.objects.get(pk=settings.LEAGUE_ID)
    # TODO: make this actually pull in teams just from the league.
    team = get_object_or_404(Team, slug=team_slug)

    try:
        profile = team.profile_team.get(slug=team_member_slug)
    except Team.DoesNotExist:
        raise Http404

    return render_response(request, 'theleague/team_member.html', {
        'schedule': team.current_schedule(league.current_season),
        'team': team,
        'profile': profile,
    })


@permission_required('theleague.change_game')
def matches(request):
    """ This will display all of the matches that have yet to be entered. """
    now = datetime.datetime.now()
    user = request.user

    # Get all of the matches in this season
    matches = Match.objects.filter(
                round__season__go_dead_date__gte=now
            ).filter(
                Q(team1=user.profile.team) | Q(team2=user.profile.team)
            ).order_by('-round__go_dead_date')

    return render_response(request, 'theleague/matches.html', {
        'matches': matches,
        })


@permission_required('theleague.change_game')
def edit_match(request, match_pk):
    """ This allows a team captain to edit a match. """
    now = datetime.datetime.now()
    user = request.user

    try:
        match = Match.objects.filter(pk=match_pk).filter(
                    Q(team1=user.profile.team) | Q(team2=user.profile.team)
                )[:1].get()
    except Match.DoesNotExist:
        raise Http404

    if match.locked:
        return render_response(request, 'theleague/edit-match.html', {
                'match': match,
                'locked': True,
            })

    else:
        final_by = match.round.go_dead_date + datetime.timedelta(hours=24)
        final = "today at %I %p" if final_by.day == now.day else "%A at %I %p"

        GameFormSet = modelformset_factory(Game, max_num=4, extra=4)

        if request.method == 'POST':
            formset = GameFormSet(request.POST)

            if formset.is_valid():
                messages.success(request, "Thanks for updating the match!")
                formset.save()
                # return redirect(...)
                pass

        else:
            formset = GameFormSet(queryset=match.game_set.all())

        return render_response(request, 'theleague/edit-match.html', {
                'formset': formset,
                'final_by': final,
                'match': match,
                'locked': False,
            })
