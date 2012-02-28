from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('apps.accounts.views',
    url(r"^authenticate/$", 'authenticate', name="authenticate"),
    url(r"^change-password/$", 'change_password', name="change-password"),
    url(r"^login/$", 'login', name="login"),
    url(r"^logout/$", 'logout', name="logout"),
)
