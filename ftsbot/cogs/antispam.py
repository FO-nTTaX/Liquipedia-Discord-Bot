#!/usr/bin/env python3

# License MIT
# Copyright 2016-2023 Alex Winkler
# Version 4.0.3

import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from ftsbot import config
from ftsbot import data
from ftsbot.ui.reportform import reportform
from unidecode import unidecode


class antispam(
	commands.Cog
):
	def __init__(
		self,
		bot
	):
		self.bot = bot
		self.reactionspammers = {}
		self.pingspammers = {}

		self.ctx_report = app_commands.ContextMenu(
			name='Report to LP Admins',
			callback=self.report,
		)
		self.bot.tree.add_command(self.ctx_report)

	async def cog_unload(
		self
	) -> None:
		self.bot.tree.remove_command(self.ctx_report.name, type=self.ctx_report.type)

	@commands.Cog.listener()
	async def on_message(
		self,
		message
	):
		if '@everyone' in message.content:
			has_exception_role = False
			for role in message.author.roles:
				if role.name in [
					'Discord Admins',
					'Liquipedia Employee',
					'Administrator',
				]:
					has_exception_role = True
					break
			if not has_exception_role:
				# give muted role
				mutedrole = discord.utils.get(message.guild.roles, name='Muted')
				await message.author.add_roles(mutedrole)
				# post message in staff channel
				reporttarget = self.bot.get_channel(config.reporttarget)
				time = message.created_at
				await reporttarget.send(
					embed=discord.Embed(
						title=(
							'Muted for potential (at)everyone spam - '
							+ message.author.mention + ' in ' + message.channel.mention
							+ ' on ' + str(time)[:-7] + ' UTC:'
						),
						color=discord.Color.blue(),
						description=(
							message.content
							# Workaround for mentions not working in embed title on windows
							+ '\n\nsource: ' + message.author.mention + ' in ' + message.channel.mention
						)
					)
				)
				# post response message so that user knows what is going on
				await message.channel.send(
					embed=discord.Embed(
						colour=discord.Colour(0xff0000),
						description=(
							message.author.mention + ' you have been muted due to trying to use (at)everyone. '
							+ 'This is a spam bot prevention. Admins will review it at their earliest convenience.'
						)
					)
				)
				# delete flagged message
				await message.delete()
		elif 'discord.gg' in message.content.lower():
			has_bad_word = False
			for bad_word in data.bad_words:
				if bad_word in message.content.lower():
					has_bad_word = True
					break
			has_exception_role = False
			for role in message.author.roles:
				if role.name in [
					'Discord Admins',
					'Liquipedia Employee',
					'Administrator',
					'Bot',
				]:
					has_exception_role = True
					break
			if has_bad_word and not has_exception_role:
				# give muted role
				mutedrole = discord.utils.get(message.guild.roles, name='Muted')
				await message.author.add_roles(mutedrole)
				# post message in staff channel
				reporttarget = self.bot.get_channel(config.reporttarget)
				time = message.created_at
				await reporttarget.send(
					embed=discord.Embed(
						title=(
							'Muted for potential discord invite link spam - '
							+ message.author.mention + ' in ' + message.channel.mention
							+ ' on ' + str(time)[:-7] + ' UTC:'
						),
						color=discord.Color.blue(),
						description=(
							message.content
							# Workaround for mentions not working in embed title on windows
							+ '\n\nsource: ' + message.author.mention + ' in ' + message.channel.mention
						)
					)
				)
				# post response message so that user knows what is going on
				await message.channel.send(
					embed=discord.Embed(
						colour=discord.Colour(0xff0000),
						description=(
							message.author.mention + ' you have been muted due to potential discord invite spam. '
							+ 'This is a spam bot prevention. Admins will review it at their earliest convenience.'
						)
					)
				)
				# delete flagged message
				await message.delete()
		else:
			cleaned_message_content = unidecode(message.content).lower()
			if 'nitro' in cleaned_message_content:
				has_exception_role = False
				for role in message.author.roles:
					if role.name in [
						'Discord Admins',
						'Liquipedia Employee',
						'Administrator',
						'Bot',
					]:
						has_exception_role = True
						break
				if not has_exception_role:
					has_additional_triggers = 0
					for trigger_word in data.nitro_spam_triggers:
						if trigger_word in cleaned_message_content:
							has_additional_triggers = has_additional_triggers + 1
					if has_additional_triggers > 1:
						# give muted role
						mutedrole = discord.utils.get(message.guild.roles, name='Muted')
						await message.author.add_roles(mutedrole)
						# post message in staff channel
						reporttarget = self.bot.get_channel(config.reporttarget)
						time = message.created_at
						await reporttarget.send(
							embed=discord.Embed(
								title=(
									'Muted for potential nitro spam - '
									+ message.author.mention + ' in ' + message.channel.mention
									+ ' on ' + str(time)[:-7] + ' UTC:'
								),
								color=discord.Color.blue(),
								description=(
									message.content
									# Workaround for mentions not working in embed title on windows
									+ '\n\nsource: ' + message.author.mention + ' in ' + message.channel.mention
								)
							)
						)
						# post response message so that user knows what is going on
						await message.channel.send(
							embed=discord.Embed(
								colour=discord.Colour(0xff0000),
								description=(
									message.author.mention + ' you have been muted due to potential nitro spam. '
									+ 'This is a spam bot prevention. Admins will review it at their earliest convenience.'
								)
							)
						)
						# delete flagged message
						await message.delete()
		if 'liquidpedia' in message.content.lower():
			await message.channel.send(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description=(
						'It is **Liquipedia**, only one d in the name! Naughty-counter of '
						+ message.author.name + ' has been incremented.'
					)
				)
			)
		if (
			hasattr(message.author, 'joined_at')
			and (discord.utils.utcnow() - message.author.joined_at).days <= 7
		):
			for role in message.role_mentions:
				if role.name == 'Liquipedia Admins':
					await message.channel.send(
						'Hello '
						+ message.author.mention
						+ ', you seem to be new to our server and you have messaged Liquipedia Administrators. '
						+ 'If your issue is not of private nature, please just write it in the channel for the game it is about.'
					)
		if (
			len(message.mentions) > 10
			and hasattr(message.author, 'joined_at')
			and (discord.utils.utcnow() - message.author.joined_at).days <= 100
		):
			has_exception_role = False
			for role in message.author.roles:
				if role.name in [
					'Discord Admins',
					'Liquipedia Employee',
					'Administrator',
					'Editor',
					'Reviewer',
					'Silver Plus',
					'Industry Person',
				]:
					has_exception_role = True
					break
			if not has_exception_role:
				if message.author.id not in self.pingspammers:
					self.pingspammers[message.author.id] = True
				else:
					try:
						await message.author.ban(reason='Automated ban, spam')
					except discord.Forbidden:
						pass

	@commands.Cog.listener()
	async def on_member_join(
		self,
		member
	):
		if (
			(
				member.name is not None
				and 'twitter.com/h0nde' in member.name.lower()
			)
			or (
				member.nick is not None
				and 'twitter.com/h0nde' in member.nick.lower()
			)
		):
			try:
				await member.ban(reason='Automated ban, spam')
			except discord.Forbidden:
				pass

	@commands.Cog.listener()
	async def on_ready(
		self
	):
		while True:
			await asyncio.sleep(60)  # Sets the time after which the reaction and ping spam lists are cleared
			self.reactionspammers.clear()
			self.pingspammers.clear()

	@commands.Cog.listener()
	async def on_reaction_add(
		self,
		reaction,
		user
	):
		# Check if user joined within last 7 days
		if hasattr(reaction.message.author, 'joined_at') and (discord.utils.utcnow() - user.joined_at).days <= 7:
			if user.id not in self.reactionspammers:
				self.reactionspammer[user.id] = 0
			self.reactionspammer[user.id] += 1
			# Take action if > 5 reactions were made in the last 60 second interval (time defined above in on_ready event)
			if self.reactionspammer[user.id] > 5:
				try:
					await reaction.message.guild.ban(user, reason='Automated ban, reaction spam')
				except discord.Forbidden:
					pass

	async def report(
		self,
		interaction: discord.Interaction,
		message: discord.Message
	):
		form = reportform(self.bot, message)
		await interaction.response.send_modal(form)
