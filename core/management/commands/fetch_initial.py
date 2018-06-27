import requests
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import get_current_timezone
from ...models import Team, Match


class Command(BaseCommand):
    help = 'fetch initial data from external api'

    def _fetch(self, url):
        try:
            r = requests.get(url)
        except:
            raise CommandError('An error occured when connecting to api')

        return r.json()

    def get_teams(self):
        url = 'http://api.football-data.org/v1/competitions/467/teams'
        result = self._fetch(url)
        return result['teams']

    def get_fixtures(self):
        url = 'http://api.football-data.org/v1/competitions/467/fixtures'
        result = self._fetch(url)
        return result['fixtures']

    def handle(self, *args, **options):
        teams = self.get_teams()
        tz = get_current_timezone()

        for team in teams:
            Team.objects.get_or_create(
                name=team['name'],
                shortname=team['code'],
                emblem=team['crestUrl'],
            )

        fixtures = self.get_fixtures()
        for item in fixtures:
            dt = datetime.strptime(item['date'], "%Y-%m-%dT%H:%M:%SZ")
            dt = tz.localize(dt)
            home_team, away_team = None, None
            home_goals, away_goals = 0, 0
            if item['homeTeamName'] and item['awayTeamName']:
                home_team = Team.objects.get(
                    name=item['homeTeamName'])
                away_team = Team.objects.get(
                    name=item['awayTeamName'])

            if item['result']:
                if item['result']['goalsHomeTeam']:
                    home_goals = int(item['result']['goalsHomeTeam'])
                if item['result']['goalsAwayTeam']:
                    away_goals = int(item['result']['goalsAwayTeam'])

            item_status = item['status'].lower()[:1]
            status = item_status if item_status in ['f', 'p', 's'] else 's'

            Match.objects.create(
                date=dt,
                home_team=home_team,
                away_team=away_team,
                home_goals=home_goals,
                away_goals=away_goals,
                status=status,
            )
