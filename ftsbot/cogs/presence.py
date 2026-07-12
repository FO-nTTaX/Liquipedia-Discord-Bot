#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 4.1.1

from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
	from ftsbot.liquipediabot import LiquipediaBot


class Presence(commands.Cog):
	def __init__(self, bot: LiquipediaBot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self) -> None:
		await self.bot.change_presence(activity=discord.Game(name='Liquipedia'))
