from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from core.models import Match, MatchTip


class PrepareDataMixin:

    def save_user(self, request, user, form):
        save_user = super().save_user(request, user, form)
        matches = Match.objects.all()
        for match in matches:
            MatchTip.objects.create(
                user=user, match=match,
            )
        return save_user


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
