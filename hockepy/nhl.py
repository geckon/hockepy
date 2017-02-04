from collections import namedtuple
from urllib.parse import urljoin

import requests

API_URL = 'https://statsapi.web.nhl.com/api/v1/'
SCHEDULE_URL = urljoin(API_URL, 'schedule')

Game = namedtuple('Game', ['home', 'away'])

def today_games():
    """Return games played in the NHL today."""
    schedule = requests.get(SCHEDULE_URL).json()
    if schedule['totalGames'] == 0:
        return []

    games = []
    for game in schedule['dates'][0]['games']:
        games.append(Game(
            home=game['teams']['home']['team']['name'],
            away=game['teams']['away']['team']['name']))
    return games

def print_today_games():
    """Print today's schedule of the NHL."""
    games = today_games()
    if not games:
        print('No games for today.')
    else:
        max_name_len = max([len(game.away) for game in games])
        for game in games:
            print('{away:>{width}} @ {home}'.format(
                away=game.away, home=game.home, width=max_name_len))

def get_schedule(date):
    """Return games played on the given date.

    Date must be in YYYY-MM-DD format. Return games as a list of Game
    named tuples.
    """
    url = '{schedule_url}?startDate={date}&endDate={date}'.format(
        schedule_url=SCHEDULE_URL, date=date)
    schedule = requests.get(url).json()
    if schedule['totalGames'] == 0:
        return []

    games = []
    for game in schedule['dates'][0]['games']:
        games.append(Game(
            home=game['teams']['home']['team']['name'],
            away=game['teams']['away']['team']['name']))
    return games
