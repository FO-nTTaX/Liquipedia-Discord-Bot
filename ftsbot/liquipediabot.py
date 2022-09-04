#!/usr/bin/env python3

# License MIT
# Copyright 2016-2022 Alex Winkler
# Version 4.0.0

import discord
from discord.ext import commands
#from ftsbot.cogs.antispam import antispam
#from ftsbot.cogs.channelmoderation import channelmoderation
#from ftsbot.cogs.presence import presence
#from ftsbot.cogs.rolecommands import rolecommands
#from ftsbot.cogs.textcommands import textcommands
from ftsbot.cogs.wikicommands import wikicommands

class liquipediabot(commands.Bot):
	def __init__(self, *, intents: discord.Intents):
		super().__init__(intents=intents, command_prefix='', help_command=None)

	async def startup(self):
		await self.wait_until_ready()
		await self.tree.sync()

	async def setup_hook(self):
		#bot.add_cog(antispam(bot))
		#bot.add_cog(channelmoderation(bot))
		#bot.add_cog(presence(bot))
		#bot.add_cog(rolecommands(bot))
		#bot.add_cog(textcommands(bot))
		await self.add_cog(wikicommands(self))
		self.loop.create_task(self.startup())
