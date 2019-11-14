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


ESCAPE_SEQ = {
    'bold': '\033[1m',
    'end': '\033[0m'
}


def bold_escape_seq_width():
    """Width of the escape sequences for bold text."""
    return len(ESCAPE_SEQ['bold']) + len(ESCAPE_SEQ['end'])


def bold_text(text):
    """Wrap a string with escape sequences for bold."""
    return f"{ESCAPE_SEQ['bold']}{text}{ESCAPE_SEQ['end']}"


def datetime_to_local(dto):
    """Convert the given datetime object to the local time zone."""
    return dto.astimezone(local_timezone())


def exit_error(msg=None):
    """Exit with an error message (if provided).

    This should be called in case of a failure that is supposed to
    lead to the program's exit.
    """
    if msg:
        logging.error(msg)
    logging.info('Exiting...')
    sys.exit(1)


def local_timezone():
    """Return local time zone as a datetime.timezone object."""
    local_time = time.localtime()
    local_tz = datetime.timezone(
        datetime.timedelta(seconds=local_time.tm_gmtoff), local_time.tm_zone
    )
    logging.debug('Local timezone is determined to be %s.', local_tz)
    return local_tz
