import datetime

from django.contrib import messages

from app_utils.tools import render_response
from apps.theleague.models import Season


def index(request):
    """ Display a list of places.
    """
    return render_response(request, 'pages/index.html', {  })


def rules(request):
    """ Display a list of places.
    """
    return render_response(request, 'pages/rules.html', {})
