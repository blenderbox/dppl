from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from apps.accounts.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    fk_name = 'user'
    max_num = 1
    verbose_name = "Profile"
    verbose_name_plural = "Profile"
    can_delete = False
    readonly_fields = ('mu', 'sigma', 'exposure')


class CustomUserAdmin(UserAdmin):
    collapse = ("collapse",)
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email'),
            },
        ),
        ("Personal Information", {
            'classes': collapse,
            'fields': (('first_name', 'last_name'),),
            },
        ),
        ("Permissions", {
            'classes': collapse, 'fields': (
                'is_active', 'is_staff', 'is_superuser', 'user_permissions'),
            },
        ),
        ("Dates", {
            'classes': collapse, 'fields': (('last_login', 'date_joined'),),
            },
        ),
        ("Groups", {
            'classes': collapse, 'fields': ('groups',),
            },
        ),
    )
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name',
            'is_staff', 'is_active')
    readonly_fields = ('password', 'last_login', 'date_joined')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
