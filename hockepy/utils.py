# vim: set fileencoding=utf-8 :

#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.utils
-------------

This module implements various utils generally useful in hockepy.

These functions are implemented:
- bold_text() -  wraps a string with escape sequences for bold
- datetime_to_local() - converts specified datetime object to local time
- exit_error() - exit with an error
- local_timezone() - return local time zone
"""

import datetime
import logging
import time
import sys


class ESCAPE_SEQ:
    BOLD = '\033[1m'
    END = '\033[0m'


def bold_text(text):
    """Wrap a string with escape sequences for bold."""
    return ESCAPE_SEQ.BOLD + text + ESCAPE_SEQ.END


def datetime_to_local(dto):
    """Convert the given datetime object to the local time zone."""
    return dto.astimezone(local_timezone())


def exit_error(msg):
    """Exit with an error message.

    This should be called in case of a failure that is supposed to
    lead to the program's exit.
    """
    logging.error(msg)
    logging.info('Exiting...')
    sys.exit(1)


def local_timezone():
    """Return local time zone as a datetime.timezone object."""
    if time.daylight:
        offset = time.altzone
        tz_name = time.tzname[1]
    else:
        offset = time.timezone
        tz_name = time.tzname[0]

    # for some reason time.timezone/altzone return a reverse offset
    offset = -1 * offset

    local_tz = datetime.timezone(datetime.timedelta(seconds=offset), tz_name)
    logging.debug(f'Local timezone is determined to be {local_tz}.')
    return local_tz
