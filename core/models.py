from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class OddBaseModel(models.Model):
    home_goals = models.IntegerField(default=0)
    away_goals = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True

    def get_odd_score(self) -> str:
        if self.home_goals == self.away_goals:
            return 'x'

        return '1' if self.home_goals > self.away_goals else '2'


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    shortname = models.CharField(max_length=3)
    emblem = models.UrlField()

    def __str__(self) -> str:
        return f'({self.shortname}) {self.name}'


class Match(OddBaseModel):
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    home_team = models.ForeignKey(Team)
    away_team = models.ForeignKey(Team)

    def __str__(self) -> str:
        home = self.home_team.shortname
        away = self.away_team.shortname
        return f'{home}-{away}'

    def get_odd_score(self) -> str:
        if self.home_goals == self.away_goals:
            return 'x'

        return '1' if self.home_goals > self.away_goals else '2'

    def get_winner(self):
        if self.home_goals == self.away_goals:
            return None

        return '1' if self.home_goals > self.away_goals else '2'


class MatchTip(OddBaseModel):
    match = models.ForeignKey(Match)
    user = models.ForeignKey(User)

    def exact_score(self) -> bool:
        if self.home_goals == match.home_goals and
        self.away_goals == match.away_goals:
            return True

        return False

    def won(self) -> bool:
        tip = self.get_odd_score()
        score = self.match.get_odd_score()
        return tip == score

    def get_score(self) -> int:
        if self.exact_score():
            return settings.EXACT_SCORE_REWARD

        if self.won():
            return settings.WINNER_REWARD

        return settings.LOSE_REWARD
