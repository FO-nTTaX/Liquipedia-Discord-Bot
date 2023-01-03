#!/usr/bin/env python3

# License MIT
# Copyright 2016-2023 Alex Winkler
# Version 4.0.3

import discord
from discord import app_commands
from discord.ext import commands
from ftsbot import data
from ftsbot.functions import autocomplete, wikifunctions
import typing


class wikicommands(
	commands.Cog
):
	def __init__(
		self,
		bot
	):
		self.bot = bot

	@app_commands.command(
		description='See pending changes'
	)
	@app_commands.describe(
		wiki='Which wiki do you want the pending changes of?',
	)
	@app_commands.autocomplete(
		wiki=autocomplete.wiki
	)
	async def pendingchanges(
		self,
		interaction: discord.Interaction,
		wiki: typing.Optional[str]
	):
		usewiki = None
		if wiki in data.wikis:
			usewiki = wiki
		elif isinstance(interaction.channel, discord.channel.TextChannel) and interaction.channel.name in data.wikis:
			usewiki = interaction.channel.name
		if usewiki is not None:
			result = wikifunctions.pendingchanges(usewiki)
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0x00ff00),
					description=result
				)
			)
		else:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='There seems to be no wiki with such a url!'
				)
			)

	@app_commands.command(
		description='See unreviewed pages'
	)
	@app_commands.describe(
		wiki='Which wiki do you want the unreviewed pages of?',
	)
	@app_commands.autocomplete(
		wiki=autocomplete.wiki
	)
	async def unreviewedpages(
		self,
		interaction: discord.Interaction,
		wiki: typing.Optional[str]
	):
		usewiki = None
		if wiki in data.wikis:
			usewiki = wiki
		elif isinstance(interaction.channel, discord.channel.TextChannel) and interaction.channel.name in data.wikis:
			usewiki = interaction.channel.name
		if usewiki is not None:
			result = wikifunctions.unreviewedpages(usewiki)
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0x00ff00),
					description=result
				)
			)
		else:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='There seems to be no wiki with such a url!'
				)
			)

	@app_commands.command(
		description='Search Liquipedia'
	)
	@app_commands.describe(
		search='What do you want to search?',
		wiki='Which wiki do you want to search?',
	)
	@app_commands.autocomplete(
		wiki=autocomplete.wiki
	)
	async def search(
		self,
		interaction: discord.Interaction,
		search: str,
		wiki: typing.Optional[str]
	):
		usewiki = None
		if wiki in data.wikis:
			usewiki = wiki
		elif isinstance(interaction.channel, discord.channel.TextChannel) and interaction.channel.name in data.wikis:
			usewiki = interaction.channel.name
		if usewiki is not None:
			result = wikifunctions.search(usewiki, search)
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0x00ff00),
					description=result
				)
			)
		else:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='There seems to be no wiki with such a url!'
				)
			)
