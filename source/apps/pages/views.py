import datetime

from django.contrib import messages

from app_utils.tools import render_response


def index(request):
    """ Display a list of places.
    """
    today = datetime.date.today()

    return render_response(request, 'pages/index.html', {})
