# -*- coding: utf-8 -*-

# License MIT
# Copyright 2016-2021 Alex Winkler
# Version 3.0.0

import discord
from dislash import *
from discord.ext import commands
from ftsbot import data
from ftsbot.functions import wikifunctions

class wikicommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@slash_commands.command(description='See pending changes', options=[
		Option('wiki', 'Which wiki do you want the pending changes of?', Type.STRING)
	])
	async def pendingchanges(self, ctx, wiki=None):
		usewiki = None
		if wiki in data.wikis:
			usewiki = wiki
		elif ctx.channel.name in data.wikis:
			usewiki = ctx.channel.name
		if usewiki is not None:
			result = wikifunctions.pendingchanges(usewiki)
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description=result))
		else:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='There seems to be no wiki with such a url!'))

	@slash_commands.command(description='See unreviewed pages', options=[
		Option('wiki', 'Which wiki do you want the unreviewed pages of?', Type.STRING)
	])
	async def unreviewedpages(self, ctx, wiki=None):
		usewiki = None
		if wiki in data.wikis:
			usewiki = wiki
		elif ctx.channel.name in data.wikis:
			usewiki = ctx.channel.name
		if usewiki is not None:
			result = wikifunctions.unreviewedpages(usewiki)
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description=result))
		else:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='There seems to be no wiki with such a url!'))

	@slash_commands.command(description='Search Liquipedia', options=[
		Option('search', 'What do you want to search?', Type.STRING, required=True),
		Option('wiki', 'Which wiki do you want to search?', Type.STRING)
	])
	async def search(self, ctx, search, wiki=None):
		usewiki = None
		if wiki in data.wikis:
			usewiki = wiki
		elif ctx.channel.name in data.wikis:
			usewiki = ctx.channel.name
		if usewiki is not None:
			result = wikifunctions.search(usewiki, search)
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description=result))
		else:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='There seems to be no wiki with such a url!'))
