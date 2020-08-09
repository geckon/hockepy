     ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
    |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
      | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
      |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
     _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
    |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|

_(pronounced like hockey-py so probably something like_ /ˈhɑː.kipaɪ/_)_

[![Build Status](https://travis-ci.com/geckon/hockepy.svg?branch=master)](https://travis-ci.com/geckon/hockepy)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/88be5e28d236447b892bd9e6525bbff8)](https://app.codacy.com/app/geckon/hockepy?utm_source=github.com&utm_medium=referral&utm_content=geckon/hockepy&utm_campaign=Badge_Grade_Dashboard)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/geckon/hockepy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/geckon/hockepy/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/geckon/hockepy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/geckon/hockepy/context:python)
[![Updates](https://pyup.io/repos/github/geckon/hockepy/shield.svg)](https://pyup.io/repos/github/geckon/hockepy/)

**Important:** Please keep in mind that `hockepy` is under active development
and any part can be changed anytime.

## Installation

```
pip install hockepy
```

## CLI utility

The main purpose of `hockepy` is to provide a command line utility for geeky
hockey fans. The easiest way to discover the features currently implemented is
to display help:

      $ hockepy -h
    usage: hocke.py [-h] [-D] [-v] {today,schedule} ...

    positional arguments:
      {today,schedule}

    optional arguments:
      -h, --help        show this help message and exit
      -D, --debug       turn debug output on
      -v, --verbose     turn verbose output on

Subcommands also support `-h` option:

    $ hockepy schedule -h
    usage: hocke.py schedule [-h] [--home-first] [--utc]
                               [first_date] [last_date]

    positional arguments:
      first_date    first date to get schedule for
      last_date     last date to get schedule for

    optional arguments:
      -h, --help    show this help message and exit
      --home-first  print the home team first
      --utc         print times in UTC instead of local time

Bear in mind that the actual help may differ as this listing won't necessarily
be updated with any feature addition/change.

### Configuration

You can highlight your favorite team using a configuration file called
`.hockepy.conf` (an example is included in the repository):

```
highlight_teams = [
    "Boston Bruins",
    "Pittsburgh Penguins",
]
```

The file can be placed in the current working directory, your home directory or
in a directory specified by HOCKEPY_CONF_DIR (hockepy checks in that order).

## NHL API

Another goal is to offer a Python interface to a subset of NHL API. Other
leagues may or may not be added as well but the main plan is to support NHL for
now.

NHL API is available at <https://statsapi.web.nhl.com/api/v1/>. I am not aware
of any available documentation so it's been discovering and trial-and-error for
me so far. If you know about any documentation, let me know.

Please note that any usage of the API (and therefore usage of `hockepy` as
well) is likely subject to
[NHL Terms of Service](https://www.nhl.com/info/terms-of-service).
