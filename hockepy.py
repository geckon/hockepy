#!/usr/bin/env python3
#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

import argparse
import logging
import sys

from hockepy.commands import get_commands
from hockepy.log import init_log


def run_hockepy():
    """Process arguments and run the specified sub(command)."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--debug', action='store_const', dest='loglevel',
                        const=logging.DEBUG, default=logging.WARNING,
                        help='turn debug output on')
    parser.add_argument('-v', '--verbose', action='store_const',
                        dest='loglevel', const=logging.INFO,
                        help='turn verbose output on')
    subparsers = parser.add_subparsers(dest='command_name')

    cmds = get_commands()
    for _, cmd_instance in cmds.items():
        cmd_instance.register_parser(subparsers)

    args = parser.parse_args(sys.argv[1:])
    if args.command_name is None:
        print("Command missing. Run `{} -h' for help.".format(sys.argv[0]))
        sys.exit(1)

    init_log(level=args.loglevel)
    logging.debug('Discovered commands: %s', cmds.keys())

    command = cmds[args.command_name]
    command.run(args)
    sys.exit(0)


if __name__ == '__main__':
    run_hockepy()
