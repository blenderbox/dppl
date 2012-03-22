from django import forms

from django.contrib.auth.models import User

from apps.accounts.models import Profile
from app_utils.widgets import BetterImageWidget


def stripped(obj, field, default=""):
    return obj.cleaned_data.get(field, default).strip()


def placeholder(text):
    """ This is just a shortcut for the TextInput widget. """
    return forms.TextInput(attrs={'placeholder': text})


class ProfileForm(forms.ModelForm):
    """ This is the basic profile form for updating a user profile. """
    error_css_class = "error"

    class Meta:
        model = Profile
        fields = ["avatar", "bio", "twitter", "facebook", "linked_in",
                "website"]
        widgets = {
                'avatar': BetterImageWidget,
                'twitter': placeholder("your_username"),
                'facebook': placeholder("your_username or "
                                        "profile.php?id=123456"),
                'linked_in': placeholder("in/your-name or "
                                         "pub/your-name/12/345/678"),
                'website': placeholder("onetinyhand.com"),
                }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['bio'].label += ':'
        self.fields['avatar'].label += ':'
        self.fields['twitter'].label = "http://twitter.com/#!/"
        self.fields['facebook'].label = "http://facebook.com/"
        self.fields['linked_in'].label = "http://www.linkedin.com/"
        self.fields['website'].label = "http://"

    def clean_twitter(self):
        """ Sanitizes the '@' and trailing whitespace from the twitter handle.
        """
        data = stripped(self, 'twitter')
        if data.startswith('@'):
            data = data[1:]
        return data

    def clean_facebook(self):
        return stripped(self, 'facebook')

    def clean_bio(self):
        return stripped(self, 'bio')


class EmailForm(forms.ModelForm):
    """ This is the basic form for updating the user's email. """
    error_css_class = "error"

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.email

    def save(self, *args, **kwargs):
        pass

    def clean_email(self):
        data = stripped(self, 'email')
        email_exists = User.objects.filter(email=data).exclude(
                pk=self.instance.pk).exists()
        if email_exists:
            raise forms.ValidationError("A user with that email address "
                    "already exists.")
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        if not self.instance.check_password(data):
            raise forms.ValidationError("The password you entered is "
                    "incorrect. Please try again.")
        return data
