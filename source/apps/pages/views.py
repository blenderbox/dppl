import datetime

from django.conf import settings
from django.contrib import messages

from app_utils.tools import render_response
from apps.theleague.models import League, Season


def index(request):
    """ Display the current round
    """
    today = datetime.datetime.today()
    league = League.objects.get(pk=settings.LEAGUE_ID)
    season = league.current_season
    rounds = []
    if season is not None:
      rounds = season.round_set\
                  .filter(go_live_date__lte=today)\
                  .order_by('-go_live_date')[:1]
    r = None
    if len(rounds) > 0:
        r = rounds[0]

    return render_response(request, 'pages/index.html', { 'current_round':r })


def rules(request):
    """ Display a list of places.
    """
    return render_response(request, 'pages/rules.html', {})
