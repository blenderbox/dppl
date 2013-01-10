from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from source.app_utils.tools import render_json, render_response
from source.apps.accounts.forms import ProfileForm, EmailForm


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
            'message': "Your email or password is incorrect.",
            }

    return render_json(context)


def login(request):
    """ This is the fallback page when a user attempts to access a page and
    they aren't logged in. Pass it the get variable "next" to have the user
    redirected once they've successfully logged in.
    """
    error = ""
    next = request.REQUEST.get('next', "/").strip()

    if request.user.is_authenticated():
        return redirect("/")
    elif request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect(next)
            else:
                error = "Your account is inactive."
        else:
            error = "Your email or password is incorrect."

    return render_response(request, "accounts/login.html", {
        'next': next,
        'error': error,
        })


@require_POST
def logout(request):
    """ This view requires a POST, and handles a logout. It returns a redirect
    to the root URL with an appended '?logout' to bust cache.
    """
    auth.logout(request)
    return redirect("/?out")


@login_required
def update_profile(request):
    """ This allows a user to update his or her profile. """
    profile_kwargs = {
            'instance': request.user.profile,
            'prefix': 'profile',
            }
    email_kwargs = {
            'instance': request.user,
            'prefix': 'email',
            }

    if request.method == 'POST':
        if profile_kwargs['prefix'] in request.POST:
            profile_form = ProfileForm(request.POST, request.FILES,
                    **profile_kwargs)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Your profile has been successfully "
                        "updated")
                return redirect("accounts:edit_profile")
            email_form = EmailForm(**email_kwargs)

        elif email_kwargs['prefix'] in request.POST:
            email_form = EmailForm(request.POST, **email_kwargs)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Your email address has been "
                        "successfully updated.")
                return redirect("accounts:edit_profile")
            profile_form = ProfileForm(**profile_kwargs)

    else:
        profile_form = ProfileForm(**profile_kwargs)
        email_form = EmailForm(**email_kwargs)

    return render_response(request, "accounts/edit-profile.html", {
        'profile_form': profile_form,
        'email_form': email_form,
        })
