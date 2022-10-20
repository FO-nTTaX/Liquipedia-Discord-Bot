#!/usr/bin/env python3

# License MIT
# Copyright 2016-2022 Alex Winkler
# Version 4.0.2

import discord
from discord import app_commands
from discord.ext import commands
from ftsbot import config, data
import typing


class channelmoderation(
	commands.Cog
):
	def __init__(
		self,
		bot
	):
		self.bot = bot

	@app_commands.command(
		description='Purge channel (admin only)'
	)
	@app_commands.describe(
		channel='Which channel do you want to purge?',
	)
	@app_commands.checks.has_any_role(
		'Discord Admins',
		'Liquipedia Employee',
		'Administrator'
	)
	@app_commands.guild_only()
	async def channelpurge(
		self,
		interaction: discord.Interaction,
		channel: typing.Optional[discord.TextChannel]
	):
		if channel is None:
			channel = interaction.channel
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x00ff00),
				description='Channel ' + channel.name + ' is being purged'
			)
		)
		if channel is None or not channel.name.startswith('temp_'):
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='Invalid channel'
				)
			)
		else:
			async for message in channel.history():
				await message.delete()

	@app_commands.command(
		description='Creates a temp. private channel and invites the specified user to it (admin only)'
	)
	@app_commands.describe(
		member='Who do you want to invite?',
	)
	@app_commands.checks.has_any_role(
		'Discord Admins',
		'Liquipedia Employee',
		'Administrator'
	)
	@app_commands.guild_only()
	async def channelcreate(
		self,
		interaction: discord.Interaction,
		member: discord.Member
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x00ff00),
				description='Channel with ' + member.name + ' is being created'
			)
		)
		guild = interaction.guild
		admin_role1 = discord.utils.get(guild.roles, name='Discord Admins')
		admin_role2 = discord.utils.get(guild.roles, name='Liquipedia Employee')
		admin_role3 = discord.utils.get(guild.roles, name='Administrator')
		overwrites = {
			guild.default_role: discord.PermissionOverwrite(read_messages=False),
			guild.me: discord.PermissionOverwrite(read_messages=True),
			member: discord.PermissionOverwrite(read_messages=True)
		}
		if admin_role1 is not None:
			overwrites[admin_role1] = discord.PermissionOverwrite(read_messages=True)
		if admin_role2 is not None:
			overwrites[admin_role2] = discord.PermissionOverwrite(read_messages=True)
		if admin_role3 is not None:
			overwrites[admin_role3] = discord.PermissionOverwrite(read_messages=True)
		channel = await guild.create_text_channel(
			'temp_' + member.name,
			overwrites=overwrites,
			category=self.bot.get_channel(int(config.privcat))
		)
		await channel.send('This channel was created to discuss the private request of ' + member.mention)

	@app_commands.command(
		description='Copies the specified temp. or active channel to the archive (admin only)'
	)
	@app_commands.describe(
		channel='Where do you want to copy things from?',
	)
	@app_commands.checks.has_any_role(
		'Discord Admins',
		'Liquipedia Employee',
		'Administrator'
	)
	@app_commands.guild_only()
	async def channelcopy(
		self,
		interaction: discord.Interaction,
		channel: typing.Optional[discord.TextChannel]
	):
		if channel is None:
			channel = interaction.channel
		if channel is None or not channel.name.startswith('temp_'):
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='Invalid channel'
				)
			)
		else:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0x00ff00),
					description='Messages have been archived'
				)
			)
			emptyarray = []
			logtarget = self.bot.get_channel(config.logtarget)
			async for message in channel.history(limit=10000, oldest_first=True):
				time = message.created_at
				embed = discord.Embed(
					title=message.author.display_name + ' on ' + str(time)[:-7] + ' UTC:',
					color=discord.Color.blue(),
					description=message.content
				)
				await logtarget.send(embed=embed)
				if message.attachments != emptyarray:
					files = message.attachments
					for file in files:
						await logtarget.send(file.url)

	@app_commands.command(
		description='Copies the specified temp. or active channel to the archive and deletes it (admin only)'
	)
	@app_commands.describe(
		channel='Which channel do you want to delete?',
	)
	@app_commands.checks.has_any_role(
		'Discord Admins',
		'Liquipedia Employee',
		'Administrator'
	)
	@app_commands.guild_only()
	async def channelkill(
		self,
		interaction: discord.Interaction,
		channel: typing.Optional[discord.TextChannel]
	):
		if channel is None:
			channel = interaction.channel
		if channel is None or not channel.name.startswith('temp_'):
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='Invalid channel'
				)
			)
		else:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0x00ff00),
					description='Messages have been archived'
				)
			)
			emptyarray = []
			logtarget = self.bot.get_channel(config.logtarget)
			async for message in channel.history(limit=10000, oldest_first='true'):
				time = message.created_at
				embed = discord.Embed(
					title=message.author.name + ' on ' + str(time)[:-7] + ' UTC:',
					color=discord.Color.blue(),
					description=message.content
				)
				await logtarget.send(embed=embed)
				if message.attachments != emptyarray:
					files = message.attachments
					for file in files:
						await logtarget.send(file.url)
			await channel.delete()
