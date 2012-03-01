from django.contrib import auth
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from app_utils.tools import render_json, render_response


@require_POST
def authenticate(request):
    """ This view requires a POST, and handles a login attempt. It will return
    a JSON response, so it is best used with AJAX.

    Args:
        request: Automatically passed by django. This should contain a username
            and password as part of the POST dictionary.

    Returns:
        A JSON response with the keys 'success' and 'message', or 'success' and
        'user' if the log in was successful.

        success: True if the user is logged in. False if the user is inactive
            or the username or password is incorrect.
        message: If unsuccessful, this will be an error message.
        user: A user object in JSON if successful.
    """
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()

    user = auth.authenticate(email=email, password=password)

    if user is not None:
        if user.is_active:  # Successful login
            auth.login(request, user)
            context = {
                'success': True,
                'user': {
                    'name': user.profile.full_name,
                    # Ranking, or other info?
                    },
                }
        else:  # Failed login, inactive account
            context = {
                'success': False,
                'message': "Your account is inactive.",
                }
    else:  # Failed login, wrong username or password
        context = {
            'success': False,
            'message': "Your username or password is incorrect.",
            }

    return render_json(context)


def login(request):
    """ This is the fallback page when a user attempts to access a page and
    they aren't logged in. Pass it the get variable "next" to have the user
    redirected once they've successfully logged in.
    """
    if request.user.is_authenticated():
        return redirect("/")
    return render_response(request, "profile/login.html", {
        'next': request.GET.get('next', "/?in").strip(),
        })


@require_POST
def logout(request):
    """ This view requires a POST, and handles a logout. It returns a redirect
    to the root URL with an appended '?logout' to bust cache.
    """
    auth.logout(request)
    return redirect("/?out")
