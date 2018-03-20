# vim: set fileencoding=utf-8 :

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
from datetime import datetime, timezone
from urllib.parse import urljoin

import requests

# URL to the NHL API
API_URL = 'https://statsapi.web.nhl.com/api/v1/'

# schedule API point
SCHEDULE_URL = urljoin(API_URL, 'schedule')

# Date/time used by the API
DATETIME_FMT = '%Y-%m-%dT%H:%M:%SZ'

Game = namedtuple('Game',
                  ['home',   # home team
                   'away',   # away team
                   'time',   # UTC time and date (datetime object)
                   'type'])  # PR/R/P (pre-season, regular, playoffs)


def log_bad_response_msg(response):
    """Try and log an error message from a bad response.

    If a bad response comes back from the NHL API, there might be
    an error message in it. If it's the case, retrieve and log it if
    possible. Do nothing if not.
    """
    # Do something for bad responses only.
    if response.status_code == requests.codes['ok']:
        return

    try:
        json = response.json()
        msg_number = json.get('messageNumber', None)
        msg = json.get('message', None)
        logging.debug('Bad response from NHL API (HTTP %d): #%d: %s',
                      response.status_code, msg_number, msg)
    except ValueError:
        logging.debug('Bad response from NHL API (HTTP %d).',
                      response.status_code)


def parse_schedule(schedule):
    """Return games played according to the schedule.

    The schedule is expected in JSON format as returned from the NHL API
    exactly. Return games as an ordered dictionary where keys are dates
    and values are lists of Game named tuples. Return None if there are
    no games in the given schedule.
    """
    if schedule['totalGames'] == 0:
        logging.debug('No games for the period of time.')
        return None

    sched = OrderedDict()
    for day in schedule['dates']:
        games = []
        for game in day['games']:
            # try and parse time
            try:
                gametime = datetime.strptime(game['gameDate'], DATETIME_FMT)
            except ValueError as err:
                logging.debug('Unable to parse time: %s', err)
                gametime = None

            # set timezone (NHL API uses UTC)
            gametime = gametime.replace(tzinfo=timezone.utc)

            games.append(Game(
                home=game['teams']['home']['team']['name'],
                away=game['teams']['away']['team']['name'],
                time=gametime,
                type=game['gameType']))
        sched[day['date']] = games
        logging.debug("Schedule found: %s", sched)
    return sched


def get_schedule(start_date, end_date):
    """Return games played between the given dates.

    Dates must be strings in "YYYY-MM-DD" format. Return games as
    an ordered dictionary where keys are dates and values are lists of
    Game named tuples. Return None if there are no games between
    the given dates.
    """
    logging.info('Retrieving NHL schedule for %s - %s.', start_date, end_date)
    url = '{schedule_url}?startDate={start}&endDate={end}'.format(
        schedule_url=SCHEDULE_URL, start=start_date, end=end_date)
    response = requests.get(url)
    if response.status_code != requests.codes['ok']:
        log_bad_response_msg(response)
        response.raise_for_status()

    return parse_schedule(response.json())
