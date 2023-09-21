import factory

from account_tiers.models import AccountTier, BasicAccountTierChoices


class AccountTierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccountTier

    name = BasicAccountTierChoices.BASIC
    thumbnail_sizes = [200, 400]
