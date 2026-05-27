#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 4.1.1

from __future__ import annotations

from collections import defaultdict, deque
from datetime import timedelta
from typing import TYPE_CHECKING
import re

import discord
from discord import app_commands
from discord.ext import commands, tasks
from unidecode import unidecode

from ftsbot import config, data
from ftsbot.ui.reportform import ReportForm
from ftsbot.utils.roles import member_has_any_named_role

if TYPE_CHECKING:
	from ftsbot.liquipediabot import LiquipediaBot


class AntiSpam(commands.Cog):
	LAST_MESSAGE_BUFFER = 50
	SAME_MESSAGE_HITS_REQUIRED = 7
	REACTION_SPAM_LIMIT = 15
	MASS_MENTION_LIMIT = 10
	NEW_USER_DAYS_FOR_ADMIN_PING_WARNING = 7
	NEW_USER_DAYS_FOR_MASS_PING_WATCH = 100

	def __init__(self, bot: LiquipediaBot):
		self.bot = bot
		self.reactionspammers: dict[int, int] = {}
		self.pingspammers: set[int] = set()

		# Track the last N messages globally to detect repeated message spam
		self.message_history: deque[discord.Message] = deque(maxlen=self.LAST_MESSAGE_BUFFER)

		# Regex to catch fake steamcommunity links often used in phishing scams
		self.steam_scam_regex = re.compile(r'\[steamcommunity\.com.*?\]\(https?://(?!steamcommunity\.com)')

		self.ctx_report = app_commands.ContextMenu(
			name='Report to LP Admins',
			callback=self.report,
		)
		self.bot.tree.add_command(self.ctx_report)

	async def cog_load(self) -> None:
		self.clear_spam_trackers.start()

	def cog_unload(self) -> None:
		self.clear_spam_trackers.cancel()
		self.bot.tree.remove_command(self.ctx_report.name, type=self.ctx_report.type)

	@tasks.loop(seconds=60)
	async def clear_spam_trackers(self) -> None:
		# Reset the spam trackers every minute to prevent accumulating false positives over time
		self.reactionspammers.clear()
		self.pingspammers.clear()

	@clear_spam_trackers.before_loop
	async def before_clear_spam_trackers(self) -> None:
		await self.bot.wait_until_ready()

	def _is_recent_member(self, member: discord.Member, *, max_days: int) -> bool:
		return member.joined_at is not None and (discord.utils.utcnow() - member.joined_at).days <= max_days

	def _has_antispam_exception_role(self, member: discord.Member) -> bool:
		return member_has_any_named_role(member, data.antispam_exception_roles)

	def _has_mass_ping_exception_role(self, member: discord.Member) -> bool:
		return member_has_any_named_role(member, data.mass_ping_exception_roles)

	def _contains_discord_invite(self, content: str) -> bool:
		content_lower = content.lower()
		return any(domain in content_lower for domain in data.discord_invite_domains)

	async def _send_report(self, title_prefix: str, message: discord.Message) -> None:
		report_channel = self.bot.get_channel(config.reporttarget)
		if not isinstance(report_channel, discord.TextChannel):
			return

		description = message.content if message.content else '*No text content*'

		await report_channel.send(
			embed=discord.Embed(
				title=f'{title_prefix} - {message.author.mention} in {message.channel.mention}',
				color=discord.Color.blue(),
				description=(f'{description}\n\nsource: {message.author.mention} in {message.channel.mention}'),
				timestamp=message.created_at,
			)
		)

	async def _send_channel_notice(self, channel: discord.abc.Messageable, *, description: str) -> None:
		try:
			await channel.send(embed=discord.Embed(colour=discord.Colour(0xFF0000), description=description))
		except (discord.Forbidden, discord.HTTPException):
			pass

	async def _delete_message(self, message: discord.Message) -> None:
		try:
			await message.delete()
		except (discord.Forbidden, discord.NotFound, discord.HTTPException):
			pass

	async def _bulk_delete_messages(self, messages: list[discord.Message]) -> None:
		"""Groups messages by channel and safely performs a bulk deletion to avoid rate limits."""
		messages_by_channel: dict[discord.abc.Messageable, list[discord.Message]] = defaultdict(list)
		for msg in messages:
			messages_by_channel[msg.channel].append(msg)

		for channel, msgs in messages_by_channel.items():
			if len(msgs) == 1:
				await self._delete_message(msgs[0])
				continue

			if hasattr(channel, 'delete_messages'):
				try:
					await channel.delete_messages(msgs)
				except discord.HTTPException:
					# Fallback to individual deletions if bulk deletion fails (e.g. messages older than 14 days)
					for msg in msgs:
						await self._delete_message(msg)
			else:
				# Fallback for channels that do not support bulk deletion (like DMs)
				for msg in msgs:
					await self._delete_message(msg)

	async def _timeout_member(self, member: discord.Member, *, reason: str) -> None:
		try:
			await member.timeout(timedelta(weeks=1), reason=reason)
		except (discord.Forbidden, discord.HTTPException):
			pass

	async def _ban_member(self, member: discord.Member, *, reason: str) -> None:
		try:
			await member.ban(reason=reason)
		except (discord.Forbidden, discord.HTTPException):
			pass

	async def _timeout_and_report(
		self,
		message: discord.Message,
		*,
		report_title: str,
		user_notice: str,
		reason: str,
	) -> None:
		if not isinstance(message.author, discord.Member):
			return

		await self._timeout_member(message.author, reason=reason)
		await self._send_report(report_title, message)
		await self._send_channel_notice(
			message.channel,
			description=(
				f'{message.author.mention} {user_notice} '
				'This is a spam bot prevention. Admins will review it at their earliest convenience.'
			),
		)

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message) -> None:
		if message.guild is None or message.author.bot or not isinstance(message.author, discord.Member):
			return

		content_lower = message.content.lower()
		normalized_content = unidecode(message.content).lower()

		# Block unauthorized @everyone or @here pings
		if ('@everyone' in content_lower or '@here' in content_lower) and not self._has_antispam_exception_role(
			message.author
		):
			await self._timeout_and_report(
				message,
				report_title='Muted for potential @everyone spam',
				user_notice='you have been muted due to trying to use @everyone or @here.',
				reason='Automated timeout, @everyone spam',
			)
			await self._delete_message(message)
			return

		# Block bad words combined with Discord invites (likely NSFW/crypto server spam)
		if self._contains_discord_invite(message.content):
			has_bad_word = any(bad_word in content_lower for bad_word in data.bad_words)
			if has_bad_word and not self._has_antispam_exception_role(message.author):
				await self._timeout_and_report(
					message,
					report_title='Muted for potential discord invite link spam',
					user_notice='you have been muted due to potential discord invite spam.',
					reason='Automated timeout, discord invite spam',
				)
				await self._delete_message(message)
				return

		# Block malicious steamcommunity phishing links
		if self.steam_scam_regex.search(content_lower):
			if not self._has_antispam_exception_role(message.author):
				await self._timeout_and_report(
					message,
					report_title='Muted for potential steam store scam link spam',
					user_notice='you have been muted due to potential steam store scam link spam.',
					reason='Automated timeout, steam scam spam',
				)
				await self._delete_message(message)
				return

		# Block "Free Discord Nitro" scams
		if 'nitro' in normalized_content and not self._has_antispam_exception_role(message.author):
			additional_triggers = sum(trigger in normalized_content for trigger in data.nitro_spam_triggers)
			if additional_triggers > 1:
				await self._timeout_and_report(
					message,
					report_title='Muted for potential nitro spam',
					user_notice='you have been muted due to potential nitro spam.',
					reason='Automated timeout, nitro spam',
				)
				await self._delete_message(message)
				return

		# Haunt people who can't spell Liquipedia
		if any(word in normalized_content for word in data.liquipedia_misspellings):
			await self._send_channel_notice(
				message.channel,
				description=(
					f'It is **Liquipedia**, please educate yourself on the spelling! '
					f'Naughty-counter of {message.author.name} has been incremented.'
				),
			)

		# Gently remind new users not to ping Liquipedia Admins directly for general issues
		if self._is_recent_member(message.author, max_days=self.NEW_USER_DAYS_FOR_ADMIN_PING_WARNING):
			for role in message.role_mentions:
				if role.name == 'Liquipedia Admins':
					await message.channel.send(
						f'Hello {message.author.mention}, you seem to be new to our server and you have messaged '
						'Liquipedia Administrators. If your issue is not of private nature, please just write it in '
						'the channel for the game it is about.'
					)
					break

		# Instaban users who spam mass mentions (e.g., raid bots pinging everyone individually)
		if (
			len(message.mentions) > self.MASS_MENTION_LIMIT
			and self._is_recent_member(message.author, max_days=self.NEW_USER_DAYS_FOR_MASS_PING_WATCH)
			and not self._has_mass_ping_exception_role(message.author)
		):
			if message.author.id in self.pingspammers:
				await self._ban_member(message.author, reason='Automated ban, ping spam')
			else:
				self.pingspammers.add(message.author.id)

		# Check for repeated message spam (someone sending the exact same text over and over)
		self.message_history.appendleft(message)

		matching_messages = [
			m for m in self.message_history if m.author == message.author and m.content == message.content
		]

		if len(matching_messages) >= self.SAME_MESSAGE_HITS_REQUIRED:
			await self._timeout_and_report(
				message,
				report_title='Muted for potential spam',
				user_notice='you have been muted due to potential spam.',
				reason='Automated timeout, repeated message spam',
			)

			await self._bulk_delete_messages(matching_messages)

			for m in matching_messages:
				try:
					self.message_history.remove(m)
				except ValueError:
					pass
			return

	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member) -> None:
		# Automatically ban specific known spam bot patterns on join
		if 'twitter.com/h0nde' in member.name.lower():
			await self._ban_member(member, reason='Automated ban, spam')
			return

		if member.nick is not None and 'twitter.com/h0nde' in member.nick.lower():
			await self._ban_member(member, reason='Automated ban, spam')

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User | discord.Member) -> None:
		# Ban new users who mass-react to messages too quickly
		if reaction.message.guild is None or user.bot or not isinstance(user, discord.Member):
			return

		if not self._is_recent_member(user, max_days=7):
			return

		self.reactionspammers[user.id] = self.reactionspammers.get(user.id, 0) + 1
		if self.reactionspammers[user.id] > self.REACTION_SPAM_LIMIT:
			await self._ban_member(user, reason='Automated ban, reaction spam')

	async def report(self, interaction: discord.Interaction, message: discord.Message) -> None:
		form = ReportForm(self.bot, message)
		await interaction.response.send_modal(form)
