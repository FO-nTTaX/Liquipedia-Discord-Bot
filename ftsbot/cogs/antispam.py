#!/usr/bin/env python3

# License MIT
# Copyright 2016-2021 Alex Winkler
# Version 3.0.0

import discord
from dislash import *
from discord.ext import commands
from ftsbot import data
import time
import datetime
import asyncio

class antispam(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.reactionspammers = {}

	@commands.Cog.listener()
	async def on_message(self, message):
		if 'liquidpedia' in message.content.lower():
			await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='It is **Liquipedia**, only one d in the name! Naughty-counter of ' + message.author.name + ' has been incremented.'))
		if (datetime.datetime.utcnow() - message.author.joined_at).days <= 7:
			for role in message.role_mentions:
				if role.name == 'Liquipedia Admins':
					await message.channel.send('Hello ' + message.author.mention + ', you seem to be new to our server and you have messaged Liquipedia Staff. If your issue is not of private nature, please just write it in the channel for the game it is about.')

	@commands.Cog.listener()
	async def on_member_join(self, member):
		if 'twitter.com/h0nde' in member.name.lower() or 'twitter.com/h0nde' in member.nick.lower():
			try:
				await member.ban(reason='Automated ban, spam')
			except discord.Forbidden:
				pass

	@commands.Cog.listener()
	async def on_ready(self):
		while True:
			await asyncio.sleep(60) # Sets the time after which the reaction spam list is cleared
			self.reactionspammers.clear()

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		# Check if user joined within last 7 days
		if (datetime.datetime.utcnow() - user.joined_at).days <= 7:
			if user.id not in self.reactionspammers:
				self.reactionspammer[user.id] = 0
			self.reactionspammer[user.id] += 1
			# Take action if > 5 reactions were made in the last 60 second interval (time defined above in on_ready event)
			if self.reactionspammer[user.id] > 5:
				try:
					await reaction.message.guild.ban(user, reason='Automated ban, reaction spam')
				except discord.Forbidden:
					pass
