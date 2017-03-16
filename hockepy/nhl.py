#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.nhl
-----------

This module implements access to a subset of NHL API.

These functions are implemented:
- get_schedule() returns games played on specified days.
"""

import logging
from collections import namedtuple, OrderedDict
from time import strptime
from urllib.parse import urljoin

import requests

# URL to the NHL API
API_URL = 'https://statsapi.web.nhl.com/api/v1/'

# schedule API point
SCHEDULE_URL = urljoin(API_URL, 'schedule')

# Date/time used by the API
DATETIME_FMT = '%Y-%m-%dT%H:%M:%SZ'

Game = namedtuple('Game',
                  ['home',  # home team
                   'away',  # away team
                   'time']) # UTC time and date (time.struct_time format)


def get_schedule(start_date, end_date):
    """Return games played between the given dates.

    Dates must be in YYYY-MM-DD format. Return games as an ordered
    dictionary where keys are dates and values are lists of Game named
    tuples. Return None if there are no games between the given dates.
    """
    logging.info('Retrieving NHL schedule for %s - %s.', start_date, end_date)
    url = '{schedule_url}?startDate={start}&endDate={end}'.format(
        schedule_url=SCHEDULE_URL, start=start_date, end=end_date)
    schedule = requests.get(url).json()
    if schedule['totalGames'] == 0:
        logging.debug('No games for the period of time.')
        return None

    sched = OrderedDict()
    for day in schedule['dates']:
        games = []
        for game in day['games']:
            # try and parse time
            try:
                gametime = strptime(game['gameDate'], DATETIME_FMT)
            except ValueError as err:
                logging.debug('Unable to parse time: %s', err)
                gametime = None

            games.append(Game(
                home=game['teams']['home']['team']['name'],
                away=game['teams']['away']['team']['name'],
                time=gametime))
        sched[day['date']] = games
    return sched
