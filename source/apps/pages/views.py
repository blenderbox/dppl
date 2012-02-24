import datetime

from django.contrib import messages

from app_utils.tools import render_response
from apps.theleague.models import Season


def index(request):
    """ Display a list of places.
    """
    today = datetime.date.today()
    # TODO: set the logic for whether the season is live or not.
    we_live_yo = False
    return render_response(request, 'pages/index.html', {
        'we_live_yo': we_live_yo
    })


def rules(request):
    """ Display a list of places.
    """
    return render_response(request, 'pages/rules.html', {})
