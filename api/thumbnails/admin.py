from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html

from images.utils import does_file_exist

from .models import Thumbnail


class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ["thumbnail_preview", "user", "thumbnail"]
    readonly_fields = ["user", "thumbnail", "image"]

    def thumbnail_preview(self, obj: Thumbnail) -> str:
        if not does_file_exist(obj.thumbnail):
            return "-"
        return format_html(
            '<img src="{url}" width=50px height=50px/>',
            url=obj.thumbnail.url,
        )

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


admin.site.register(Thumbnail, ThumbnailAdmin)
