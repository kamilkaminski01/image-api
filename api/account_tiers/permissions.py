from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from .models import AccountTier


class HasEnabledExpiringUrls(BasePermission):
    message = "Your account tier must have enabled expiring urls to perform this action"

    def has_permission(self, request: Request, view) -> bool:
        account_tier = AccountTier.objects.get(pk=request.user.account_tier.id)
        return account_tier.enabled_expiring_urls
