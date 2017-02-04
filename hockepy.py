#!/usr/bin/env python3
#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

import argparse
import sys

from hockepy import nhl
from hockepy import commands
from hockepy.commands import BaseCommand

if __name__ == '__main__':
    # default action
    if len(sys.argv) == 1 or sys.argv[1] == 'today':
        nhl.print_today_games()
        sys.exit(0)

    # other actions
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')

    CMDS = [cmd() for cmd in BaseCommand.__subclasses__()]
    for cmd in CMDS:
        cmd.register_parser(subparsers)

    args = parser.parse_args(sys.argv[1:])
    for cmd in CMDS:
        if args.subparser_name  == cmd.command:
            cmd.run(args)
            sys.exit(0)

    # unknown command
    print('Unknown command {}'.format(sys.argv[1]))
    sys.exit(1)

