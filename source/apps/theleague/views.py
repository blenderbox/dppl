import datetime

from django.contrib import messages

from app_utils.tools import render_response


def scoreboard(request):
    """ Display the scoreboard
    """
    today = datetime.date.today()

    return render_response(request, 'theleague/scoreboard.html', {})


def schedule(request):
    """ Display the schedule
    """
    today = datetime.date.today()

    return render_response(request, 'theleague/schedule.html', {})
