from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


User = get_user_model()


class BetBaseModel(models.Model):
    home_goals = models.IntegerField(default=0)
    away_goals = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True

    def get_bet_score(self) -> str:
        if self.home_goals == self.away_goals:
            return 'x'

        return '1' if self.home_goals > self.away_goals else '2'


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    shortname = models.CharField(max_length=3)
    emblem = models.URLField()

    def __str__(self) -> str:
        return self.name


class MatchQuerySet(models.QuerySet):
    # Available on both Manager and QuerySet.
    def active(self):
        now = timezone.now()
        return self.filter(date__gte=now)

    def pending(self):
        return self.filter(status=Match.PENDING)


class Match(BetBaseModel):
    PENDING = 'p'
    SCHEDULED = 's'
    FINISHED = 'f'
    MATCH_CHOICES = (
        (PENDING, _('pending')),
        (SCHEDULED, _('scheduled')),
        (FINISHED, _('finished')),
    )

    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=1,
        choices=MATCH_CHOICES, default=SCHEDULED)
    home_team = models.ForeignKey(
        Team, null=True, on_delete=models.SET_NULL,
        related_name="match_home_team"
    )
    away_team = models.ForeignKey(
        Team, null=True, on_delete=models.SET_NULL,
        related_name="match_away_team"
    )

    objects = MatchQuerySet.as_manager()

    def __str__(self) -> str:
        home = self.home_team.shortname if self.home_team else "-"
        away = self.away_team.shortname if self.away_team else "-"
        return f'{home}-{away}'

    def get_winner(self):
        if self.home_goals == self.away_goals:
            return None

        return '1' if self.home_goals > self.away_goals else '2'


class MatchTip(BetBaseModel):
    match = models.ForeignKey(
        Match, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL)

    def exact_score(self) -> bool:
        if ((self.home_goals == match.home_goals) and
        (self.away_goals == match.away_goals)):
            return True

        return False

    def won(self) -> bool:
        tip = self.get_bet_score()
        score = self.match.get_bet_score()
        return tip == score

    def get_score(self) -> int:
        if self.exact_score():
            return settings.EXACT_SCORE_REWARD

        if self.won():
            return settings.WINNER_REWARD

        return settings.LOSE_REWARD
