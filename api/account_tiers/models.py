from django.db import models

from .utils import validate_thumbnail_sizes


class BasicAccountTierChoices:
    BASIC = "Basic", "Basic"
    PREMIUM = "Premium", "Premium"
    ENTERPRISE = "Enterprise", "Enterprise"


class AccountTier(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
    )

    thumbnail_sizes = models.JSONField(
        default=list,
        validators=[validate_thumbnail_sizes],
        help_text="Comma-separated list of thumbnail sizes",
    )

    include_original_image_url = models.BooleanField(
        default=False,
        help_text="Include a url to the originally uploaded file",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Account Tier"
        verbose_name_plural = "Account Tiers"
