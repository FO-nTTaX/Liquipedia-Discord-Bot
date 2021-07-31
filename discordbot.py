# -*- coding: utf-8 -*-

# License MIT
# Copyright 2016-2021 Alex Winkler
# Version 3.0.0

import discord
from discord.ext import commands
from dislash import *
from ftsbot import secrets
from ftsbot.cogs.antispam import antispam
from ftsbot.cogs.channelmoderation import channelmoderation
from ftsbot.cogs.presence import presence
from ftsbot.cogs.rolecommands import rolecommands
from ftsbot.cogs.textcommands import textcommands
from ftsbot.cogs.wikicommands import wikicommands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!fobot', intents=intents)
SlashClient(bot)

bot.add_cog(antispam(bot))
bot.add_cog(channelmoderation(bot))
bot.add_cog(presence(bot))
bot.add_cog(rolecommands(bot))
bot.add_cog(textcommands(bot))
bot.add_cog(wikicommands(bot))

bot.run(secrets.token)
