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
- parse_schedule() returns Games as parsed from the given JSON schedule
- log_bad_response_msg() logs error message from a bad response from
    the NHL API if possible
- get_status() returns GameStatus for NHL API's statusCode
- get_type() returns GameType for NHL API's gameType
"""

import logging
from collections import OrderedDict
from datetime import datetime, timezone
from urllib.parse import urljoin

import requests

from hockepy.game import Game, GameStatus, GameType, Play

# URL to the NHL API
API_URL = 'https://statsapi.web.nhl.com/api/v1/'

# API points
FEED_URL = urljoin(API_URL, 'game/')
SCHEDULE_URL = urljoin(API_URL, 'schedule')

# Date/time used by the API
DATETIME_FMT = '%Y-%m-%dT%H:%M:%SZ'


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
        logging.debug(
            f'Bad response from NHL API (HTTP {response.status_code}): '
            f'#{msg_number}: {msg}'
        )
    except ValueError:
        logging.debug(
            f'Bad response from NHL API (HTTP {response.status_code}).'
        )


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
            status_code = game['status']['statusCode']
            if status_code == '8':
                # scheduled but time TBD
                gametime = 'TBD'
            else:
                try:
                    gametime = datetime.strptime(game['gameDate'],
                                                 DATETIME_FMT)
                    # set timezone (NHL API uses UTC)
                    gametime = gametime.replace(tzinfo=timezone.utc)
                except ValueError as err:
                    logging.debug(f'Unable to parse time: {err}')
                    gametime = None

            # retrieve last play
            lastplay = get_last_play(game['gamePk'], False)

            games.append(
                Game(
                    home=game['teams']['home']['team']['name'],
                    away=game['teams']['away']['team']['name'],
                    home_score=game['teams']['home']['score'],
                    away_score=game['teams']['away']['score'],
                    time=gametime,
                    type=get_type(game['gameType']),
                    status=get_status(status_code),
                    last_play=get_play_tuple(lastplay)
                )
            )
        sched[day['date']] = games
        logging.debug(f'Schedule found: {sched}')
    return sched


def get_status(status_code):
    """Return GameStatus for the given NHL API's statusCode."""
    if status_code in ('1', '2', '8'):
        return GameStatus.SCHEDULED
    if status_code in ('3', '4'):
        return GameStatus.LIVE
    return GameStatus.FINAL


def get_type(game_type):
    """Return GameType for the given NHL API's gameType."""
    if game_type == 'PR':
        return GameType.PRESEASON
    if game_type == 'R':
        return GameType.REGULAR
    return GameType.PLAYOFFS


def get_schedule(start_date, end_date):
    """Return games played between the given dates.

    Dates must be strings in "YYYY-MM-DD" format. Return games as
    an ordered dictionary where keys are dates and values are lists of
    Game named tuples. Return None if there are no games between
    the given dates.
    """
    logging.info(f'Retrieving NHL schedule for {start_date} - {end_date}.')
    url = f'{SCHEDULE_URL}?startDate={start_date}&endDate={end_date}'
    response = requests.get(url)
    if response.status_code != requests.codes['ok']:
        log_bad_response_msg(response)
        response.raise_for_status()

    return parse_schedule(response.json())


def get_plays(game_id, fail=True):
    """Retrieve all plays as provided in the live feed.

    Return list of all plays available in the feed in the format
    provided by the NHL API.
    If it's not possible to retrieve the feed for the given game_id,
    then it depends on fail parameter - if it's True, an exception will
    be raised, otherwise None is returned without an exception.
    """
    logging.info(f'Retrieving NHL game live feed plays for {game_id}.')
    url = urljoin(FEED_URL, f'{game_id}/feed/live')
    response = requests.get(url)
    if response.status_code != requests.codes['ok']:
        log_bad_response_msg(response)
        if fail:
            response.raise_for_status()
        return None

    return response.json()['liveData']['plays']['allPlays']


def get_play_tuple(play):
    """Get a play tuple from a play returned by the NHL API or None.

    Return a Play namedtuple for the given play and ignore other
    information about the play provided by the NHL API.
    Return None if the given play is empty or not valid.
    """
    if not play:
        return None

    period = play['about']['ordinalNum']

    mins, secs = [int(num) for num in play['about']['periodTime'].split(':')]
    mins = mins + 20 * (play['about']['period'] - 1)
    if period == 'SO':
        # if the "period" is shootout, then it's clear that we're in
        # a regular season and following after a 5 minutes long (not 20)
        # overtime -> subtract 15 minutes from the game time
        mins = mins - 15
    time = f'{mins:02d}:{secs:02d}'

    return Play(period=period, time=time,
                description=play['result']['description'])


def get_last_play(game_id, fail=True):
    """Return the last play (for the given game) in the tuple format.

    The tuple format is usually a Play named tuple or None.
    If it's not possible to retrieve the feed for the given game_id,
    then it depends on fail parameter - if it's True, an exception will
    be raised, otherwise None is returned without an exception.
    """
    logging.info(f'Retrieving NHL game last play for {game_id}.')
    url = urljoin(FEED_URL, f'{game_id}/feed/live')
    response = requests.get(url)
    if response.status_code != requests.codes['ok']:
        log_bad_response_msg(response)
        if fail:
            response.raise_for_status()
        return None

    try:
        return response.json()['liveData']['plays']['currentPlay']
    except KeyError as err:
        if fail:
            raise err
        return None
