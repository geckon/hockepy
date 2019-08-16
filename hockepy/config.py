# -*- coding: utf-8 -*-

#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.config
-------------

This module manages configuration for hockepy.

CONF dictionary is provided for any module to use.

These functions are implemented:
- read_config_file() finds and reads a config file if available
- init_config() initializes CONF dictionary, needs to be called once
"""

import os
import logging

import toml

CONF = {}

CONF_FILE_NAME = '.hockepy.conf'


def read_config_file():
    """Find and read config file (.hockepy.conf) if exists.

    Config file will be looked for in these directories in this order:
    - current working directory
    - home directory
    - directory specified by HOCKEPY_CONF_DIR environment
      variable
    Return the config file contents if found, empty dictionary
    otherwise.
    """
    env_var = 'HOCKEPY_CONF_DIR'

    locations = [
        (os.curdir, 'current directory'),
        (os.path.expanduser('~'), 'home directory'),
        (os.environ.get(env_var), f'{env_var!r} environment variable'),
    ]

    logging.debug('Looking for config file.')
    for loc, loc_desc in locations:
        try:
            logging.debug('Trying %s', loc_desc)
            cf_path = os.path.join(loc, CONF_FILE_NAME)
            cf_content = toml.load(cf_path)
            logging.info('Reading config file %r', cf_path)
            return cf_content
        except IOError as err:
            logging.debug('Could not read %r: %s', cf_path, err.strerror)
        except TypeError as err:
            logging.debug('Not found.')
        except toml.TomlDecodeError:
            logging.warning('Config file %s has a wrong format. Ingoring it.')

    logging.info('Config file not found. Default values will be used.')
    return {}


def init_config():
    """Initialize config with data from a config file if available.

    Otherwise default values will be used.
    """
    conf_file = read_config_file()

    global CONF
    # initialize default values here (if not specified by the config file):
