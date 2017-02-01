
from urllib.parse import urljoin

import requests

API_URL = 'https://statsapi.web.nhl.com/api/v1/'
SCHEDULE_URL = urljoin(API_URL, 'schedule')

def today():
    """Print today's schedule of the NHL."""
    schedule = requests.get(SCHEDULE_URL).json()
    if schedule['totalGames'] == 0:
        print('No games for today.')
    else:
        today_games = schedule['dates'][0]['games']
        for game in today_games:
            print('{away} @ {home}'.format(
                away=game['teams']['away']['team']['name'],
                home=game['teams']['home']['team']['name']))


