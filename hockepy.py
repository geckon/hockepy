#!/usr/bin/env python3

import sys
from urllib.parse import urljoin

import requests

API_URL = 'https://statsapi.web.nhl.com/api/v1/'
SCHEDULE_URL = urljoin(API_URL, 'schedule')

if __name__ == '__main__':
    schedule = requests.get(SCHEDULE_URL).json()
    if schedule['totalGames'] == 0:
        print('No games for today.')
        sys.exit(0)

    today = schedule['dates'][0]
    for game in today['games']:
        print('{away} @ {home}'.format(
            away=game['teams']['away']['team']['name'],
            home=game['teams']['home']['team']['name']))

