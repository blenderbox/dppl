from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailBackend(ModelBackend):
    """ This is a simple Authentication backend which will allow users to log
    in with their username, or email address. It was copied from:
    https://gist.github.com/586056
    Slight alterations have been made for PEP8 standards.
    """

    def authenticate(self, **credentials):
        """ Log a user in by their username or email.

        Kwargs:
            username: The user's username. If passed, this will default to the
                built-in Django authenticate method.
            email: The user's email address. If passed, we'll user our own
                method to log the user in.
            password: The user's password.

        Returns:
            A User object if the credentials are correct, and the user is
            active, otherwise None is returned.
        """
        if 'username' in credentials:
            return super(EmailBackend, self).authenticate(**credentials)

        try:
            user = User.objects.get(email=credentials.get('email'))
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(credentials.get('password')):
                return user

        return None
