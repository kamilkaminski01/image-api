from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

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
    readonly_fields = ["date_joined", "last_login"]
    ordering = ("email",)

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
