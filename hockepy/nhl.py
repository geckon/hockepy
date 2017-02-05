#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

import logging
from collections import namedtuple
from urllib.parse import urljoin

import requests

API_URL = 'https://statsapi.web.nhl.com/api/v1/'
SCHEDULE_URL = urljoin(API_URL, 'schedule')

Game = namedtuple('Game', ['home', 'away'])


def get_schedule(date):
    """Return games played on the given date.

    Date must be in YYYY-MM-DD format. Return games as a list of Game
    named tuples.
    """
    logging.debug('Retrieving NHL schedule for %s.', date)
    url = '{schedule_url}?startDate={date}&endDate={date}'.format(
        schedule_url=SCHEDULE_URL, date=date)
    schedule = requests.get(url).json()
    if schedule['totalGames'] == 0:
        logging.debug('No games for the period of time.')
        return []

    games = []
    for game in schedule['dates'][0]['games']:
        games.append(Game(
            home=game['teams']['home']['team']['name'],
            away=game['teams']['away']['team']['name']))
    return games
