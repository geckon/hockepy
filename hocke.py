#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.py
-----------

hockepy.py CLI utility implementation.

Run with -h for help.
"""

import argparse
import logging
import sys

from hockepy.commands import get_commands
from hockepy.log import init_log


def process_args(parser):
    """Parse, process and return arguments.

    Also initialize logger. Exit, if there is an error (e.g. no command
    provided).
    """
    args = parser.parse_args(sys.argv[1:])
    if args.command_name is None:
        print("Command missing. Run `{} -h' for help.".format(sys.argv[0]))
        sys.exit(1)

    if args.debug:
        loglevel = logging.DEBUG
    elif args.verbose:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING
    init_log(level=loglevel)
    logging.debug('Logging level set to %s', loglevel)

    return args


def run_hockepy():
    """Process arguments and run the specified sub(command)."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--debug', action='store_true', dest='debug',
                        help='turn debug output on')
    parser.add_argument('-v', '--verbose', action='store_true',
                        dest='verbose', help='turn verbose output on')
    subparsers = parser.add_subparsers(dest='command_name')

    cmds = get_commands()
    for _, cmd_instance in cmds.items():
        cmd_instance.register_parser(subparsers)

    args = process_args(parser)

    logging.debug('Discovered commands: %s', cmds.keys())
    # Initialize and run the requested command.
    command = cmds[args.command_name](args)
    command.run()
    sys.exit(0)


if __name__ == '__main__':
    run_hockepy()
