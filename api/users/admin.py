from typing import List

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.http import HttpRequest

from .models import User


class UsersAdmin(UserAdmin):
    exclude = ("username",)
    list_display = [
        "email",
        "first_name",
        "last_name",
        "account_tier",
        "is_staff",
    ]
    ordering = ("email",)

    def get_readonly_fields(self, request: HttpRequest, obj=None) -> List:
        if obj is None:
            return ["date_joined", "last_login"]
        else:
            return ["account_tier", "date_joined", "last_login"]

    add_fieldsets = (
        (
            "General",
            {
                "classes": ("wide",),
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "account_tier",
                    "password1",
                    "password2",
                ],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": [
                    "is_staff",
                    "is_active",
                    "date_joined",
                    "last_login",
                ],
            },
        ),
    )

    fieldsets = (
        (
            "General",
            {
                "classes": ("wide",),
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "account_tier",
                    "password",
                ],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": [
                    "is_staff",
                    "is_active",
                    "date_joined",
                    "last_login",
                ],
            },
        ),
    )


admin.site.register(User, UsersAdmin)
admin.site.unregister(Group)
