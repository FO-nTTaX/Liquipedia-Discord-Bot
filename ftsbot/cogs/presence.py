# -*- coding: utf-8 -*-

# License MIT
# Copyright 2016-2021 Alex Winkler
# Version 3.0.0

import discord
from dislash import *
from discord.ext import commands
from ftsbot import data

class presence(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		game = discord.Game(name='Liquipedia', url=data.wikibaseurl, type=1)
		await self.bot.change_presence(activity=game)