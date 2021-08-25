#!/usr/bin/env python3

# License MIT
# Copyright 2016-2021 Alex Winkler
# Version 3.0.0

import discord
from dislash import *
from discord.ext import commands
from ftsbot import config, data

class channelmoderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@slash_commands.has_any_role('Discord Admins', 'Liquipedia Employee', 'Administrator')
	@slash_commands.command(description='Purge channel (admin only)', options=[
		Option('channel', 'Which channel do you want to purge?', Type.CHANNEL)
	], guild_ids=config.guild_ids)
	async def channelpurge(self, ctx, channel=None):
		if channel is None:
			channel = ctx.channel
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='Channel ' + channel.name + ' is being purged'))
		if channel is None or not channel.name.startswith('temp_'):
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='Invalid channel'))
		else:
			async for message in channel.history():
				await message.delete()

	@slash_commands.has_any_role('Discord Admins', 'Liquipedia Employee', 'Administrator')
	@slash_commands.command(description='Creates a temp. private channel and invites the specified user to it (admin only)', options=[
		Option('member', 'Who do you want to invite?', Type.USER, required=True)
	], guild_ids=config.guild_ids)
	async def channelcreate(self, ctx, member):
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='Channel with ' + member.name + ' is being created'))
		guild = ctx.guild
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
		channel = await guild.create_text_channel('temp_' + member.name, overwrites=overwrites, category=self.bot.get_channel(int(config.privcat)))
		await channel.send('This channel was created to discuss the private request of ' + member.mention)

	@slash_commands.has_any_role('Discord Admins', 'Liquipedia Employee', 'Administrator')
	@slash_commands.command(description='Copies the specified temp. or active channel to the archive (admin only)', options=[
		Option('channel', 'Where do you want to copy things from?', Type.CHANNEL)
	], guild_ids=config.guild_ids)
	async def channelcopy(self, ctx, channel=None):
		if channel is None:
			channel = ctx.channel
		if channel is None or not channel.name.startswith('temp_'):
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='Invalid channel'))
		else:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='Messages have been archived'))
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
				if message.attachments !=emptyarray:
					files = message.attachments
					for file in files:
						await logtarget.send(file.url)

	@slash_commands.has_any_role('Discord Admins', 'Liquipedia Employee', 'Administrator')
	@slash_commands.command(description='Copies the specified temp. or active channel to the archive and deletes it (admin only)', options=[
		Option('channel', 'Which do you want to delete?', Type.CHANNEL)
	], guild_ids=config.guild_ids)
	async def channelkill(self, ctx, channel=None):
		if channel is None:
			channel = ctx.channel
		if channel is None or not channel.name.startswith('temp_'):
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='Invalid channel'))
		else:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='Messages have been archived'))
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
