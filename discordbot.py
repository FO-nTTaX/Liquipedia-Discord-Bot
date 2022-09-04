#!/usr/bin/env python3

# License MIT
# Copyright 2016-2022 Alex Winkler
# Version 4.0.0

import discord
from ftsbot.liquipediabot import liquipediabot
from ftsbot import secrets

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = liquipediabot(intents=intents)

bot.run(secrets.token)
