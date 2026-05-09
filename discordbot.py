#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 4.1.1

import os
from dotenv import load_dotenv

from ftsbot.liquipediabot import liquipediabot

load_dotenv()

bot = liquipediabot()

bot.run(os.environ.get('token').strip())
