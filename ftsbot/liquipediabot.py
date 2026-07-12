#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

from __future__ import annotations

import asyncio

import discord
from discord.ext import commands

from ftsbot import config
from ftsbot.cogs.antispam import AntiSpam
from ftsbot.cogs.channelmoderation import ChannelModeration
from ftsbot.cogs.pingcommands import PingCommands
from ftsbot.cogs.presence import Presence
from ftsbot.cogs.rolecommands import RoleCommands
from ftsbot.cogs.textcommands import TextCommands
from ftsbot.cogs.wikicommands import WikiCommands
from ftsbot.services.http import HttpClient
from ftsbot.services.mediawiki import MediaWikiService
from ftsbot.services.tlintegration import TLIntegrationService


class LiquipediaBot(commands.Bot):
	def __init__(self, *, apikey: str | None):
		intents = discord.Intents.default()
		intents.members = True
		intents.message_content = True
		intents.reactions = True

		super().__init__(intents=intents, command_prefix='!fobot', help_command=None)

		self.http_client = HttpClient()
		self.mediawiki = MediaWikiService(self.http_client)
		self.tlintegration = TLIntegrationService(self.http_client, apikey=apikey)

	async def startup(self) -> None:
		await self.wait_until_ready()
		await self.tree.sync()
		await self.tree.sync(guild=discord.Object(id=config.commandserver))

	async def setup_hook(self) -> None:
		await self.http_client.start()

		await self.add_cog(AntiSpam(self))
		await self.add_cog(ChannelModeration(self))
		await self.add_cog(PingCommands(self))
		await self.add_cog(Presence(self))
		await self.add_cog(RoleCommands(self))
		await self.add_cog(TextCommands(self))
		await self.add_cog(WikiCommands(self))

		asyncio.create_task(self.startup())

	async def close(self) -> None:
		await self.http_client.close()
		await super().close()
