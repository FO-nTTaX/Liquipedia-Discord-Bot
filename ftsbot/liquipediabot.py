#!/usr/bin/env python3

# License MIT
# Copyright 2016-2025 Alex Winkler
# Version 4.0.3

import discord
from discord.ext import commands
from ftsbot import config
from ftsbot.cogs.antispam import antispam
from ftsbot.cogs.channelmoderation import channelmoderation
from ftsbot.cogs.presence import presence
from ftsbot.cogs.rolecommands import rolecommands
from ftsbot.cogs.textcommands import textcommands
from ftsbot.cogs.wikicommands import wikicommands


class liquipediabot(
	commands.Bot
):
	def __init__(
		self
	):
		intents = discord.Intents.default()
		intents.members = True
		intents.message_content = True
		intents.reactions = True

		super().__init__(intents=intents, command_prefix='!fobot', help_command=None)

	async def startup(
		self
	):
		await self.wait_until_ready()
		await self.tree.sync()
		await self.tree.sync(guild=discord.Object(id=config.commandserver))

	async def setup_hook(
		self
	):
		await self.add_cog(antispam(self))
		await self.add_cog(channelmoderation(self))
		await self.add_cog(presence(self))
		await self.add_cog(rolecommands(self))
		await self.add_cog(textcommands(self))
		await self.add_cog(wikicommands(self))
		self.loop.create_task(self.startup())
