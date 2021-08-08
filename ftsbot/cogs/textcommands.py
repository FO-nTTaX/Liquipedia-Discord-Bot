#!/usr/bin/env python3

# License MIT
# Copyright 2016-2021 Alex Winkler
# Version 3.0.0

import random
import discord
from dislash import *
from discord.ext import commands
from ftsbot import data

class textcommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@slash_commands.cooldown(1, 300, commands.BucketType.user)
	@slash_commands.command(description='Author information')
	async def author(self, ctx):
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x663399), description='FO-BoT was coded by **FO-nTTaX**'))

	@slash_commands.command(description='On shady betting sites')
	async def betting(self, ctx):
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='[On shady betting sites](https://liquipedia.net/commons/User:FO-nTTaX/Betting)'))

	@slash_commands.command(description='Blame someone')
	async def blame(self, ctx):
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x663399), description='**#blamesalle**'))

	@slash_commands.command(description='Dance')
	async def dance(self, ctx):
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x663399), description='**EVERYBODY DANCE \\\\Ü/**\n*dances :D\\\\-<*\n*dances :D|-<*\n*dances :D/-<*'))

	@slash_commands.command(description='Roll a dice', options=[
		Option('sides', 'How many sides (default 6)?', Type.INTEGER),
		Option('amount', 'How many dice (default 1)?', Type.INTEGER)
	])
	async def dice(self, ctx, sides=6, amount=1):
		if sides < 2:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='A die needs to have a least 2 sides'))
		elif amount < 1:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='You need to roll at least one die'))
		result = ''
		if amount == 1:
			result = 'Your ' + str(sides) + '-sided die threw a ' + str(random.randrange(1, sides + 1, 1)) + '.'
		else:
			rolls = [random.randrange(1, sides + 1, 1) for _ in range(amount)]
			result = 'Your ' + str(amount) + ' ' + str(sides) + '-sided dice threw ' + str(rolls) + ' for a total of ' + str(sum(rolls)) + '.'
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x663399), description=result))

	@slash_commands.command(description='Links to guides')
	async def guides(self, ctx):
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='**Liquipedia-Guides**: https://liquipedia.net/starcraft2/User:FO-BoT#Guides'))

	@slash_commands.command(description='\\Ü/ HYPE \\Ü/')
	async def hype(self, ctx):
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x663399), description='**\\\\Ü/ HYPE \\\\Ü/**'))
		await ctx.send('https://i.imgur.com/xmdBFq9.mp4')

	@slash_commands.command(description='Tell people to just ask!')
	async def justask(self, ctx):
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='If you need help with something or just have a question, please post the question in the channel for the relevant wiki.' + 
		' Asking if someone can help only costs you extra time, and you usually don\'t even need an admin!'))

	@slash_commands.command(description='Lickypiddy!')
	async def lickypiddy(self, ctx):
		lickypiddywiki = 'commons'
		if ctx.channel.name in data.wikis:
			lickypiddywiki = ctx.channel.name
		else:
			lickypiddywiki = 'commons'
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x663399), description='[\\\\Ü/ All glory Lickypiddy \\\\Ü/](https://liquipedia.net/' + lickypiddywiki + '/Special:Lickypiddy)'))

	@slash_commands.command(description='Tell a lie')
	async def lie(self, ctx):
		i = random.randrange(0, len(data.lies), 1)
		response = data.lies[i]
		if response.startswith('http'):
			await ctx.send(response)
		else:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0x663399), description=response))

	@slash_commands.command(description='Liquipedia!')
	async def liquipedia(self, ctx):
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='**Liquipedia** is awesome!'))

	@slash_commands.command(description='Link the notability guidelines', options=[
		Option('wiki', 'Which wiki do you want the notability guidelines for?', Type.STRING)
	])
	async def notability(self, ctx, wiki=None):
		usewiki = None
		if wiki in data.wikis:
			usewiki = wiki
		elif ctx.channel.name in data.wikis:
			usewiki = ctx.channel.name
		if usewiki is not None:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='[Notability Guidelines](https://liquipedia.net/' + usewiki + '/Liquipedia:Notability_Guidelines)'))
		else:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='No wiki specified'))

	@slash_commands.command(description='Edit Statistics')
	async def ranking(self, ctx):
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='**Liquipedia ranking**: https://liquipedia.net/statistics/?view=editcount&wikilist=all'))

	@slash_commands.command(description='Think very hard')
	async def thinking(self, ctx):
		await ctx.send('https://files.catbox.moe/o8tify.gif')
