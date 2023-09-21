from typing import List

from django.contrib import admin
from django.http import HttpRequest

from .models import AccountTier


class AccountTierAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "include_original_image_url",
        "thumbnail_sizes",
        "enabled_expiring_urls",
    ]

    def get_readonly_fields(self, request: HttpRequest, obj=None) -> List:
        if obj is None:
            return []
        else:
            return [
                "name",
                "thumbnail_sizes",
                "include_original_image_url",
                "enabled_expiring_urls",
            ]

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        if obj and obj.id == 1:
            return False
        return True


admin.site.register(AccountTier, AccountTierAdmin)
