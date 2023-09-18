from django.contrib import admin
from django.utils.html import format_html

from .models import Image
from .utils import does_file_exist


class ImageAdmin(admin.ModelAdmin):
    list_display = ["image_preview", "user", "image"]

    def image_preview(self, obj: Image) -> str:
        if not does_file_exist(obj.image):
            return "-"
        return format_html(
            '<img src="{url}" width=50px height=50px/>',
            url=obj.image.url,
        )


admin.site.register(Image, ImageAdmin)