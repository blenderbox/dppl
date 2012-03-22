from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r"^authenticate/$", 'apps.accounts.views.authenticate',
        name="authenticate"),

    url(r"^change-password/complete/$",
        'django.contrib.auth.views.password_change_done',
        {'template_name': "accounts/change-password-done.html"},
        name="change_password_done"),
    url(r"^change-password/$",
        'django.contrib.auth.views.password_change',
        {'template_name': "accounts/change-password.html",
         'post_change_redirect': "accounts:change_password_done"},
        name="change_password"),

    url(r"^edit-profile/$", 'apps.accounts.views.update_profile',
        name="edit_profile"),

    url(r"^login/$", 'apps.accounts.views.login', name="login"),
    url(r"^logout/$", 'apps.accounts.views.logout', name="logout"),
)
