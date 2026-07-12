#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from ftsbot import config, data
from ftsbot.utils.embeds import error_embed, success_embed
from ftsbot.utils.interactions import defer_response, send_ephemeral

if TYPE_CHECKING:
	from ftsbot.liquipediabot import LiquipediaBot


class ChannelModeration(commands.Cog):
	def __init__(self, bot: LiquipediaBot):
		self.bot = bot

	def _resolve_text_channel(
		self,
		interaction: discord.Interaction,
		channel: discord.TextChannel | None,
	) -> discord.TextChannel | None:
		if channel is not None:
			return channel

		if isinstance(interaction.channel, discord.TextChannel):
			return interaction.channel

		return None

	def _is_temp_channel(self, channel: discord.TextChannel | None) -> bool:
		return channel is not None and channel.name.startswith('temp_')

	def _get_log_channel(self) -> discord.TextChannel | None:
		channel = self.bot.get_channel(config.logtarget)
		if isinstance(channel, discord.TextChannel):
			return channel
		return None

	async def _archive_channel(self, channel: discord.TextChannel) -> int:
		log_channel = self._get_log_channel()
		if log_channel is None:
			raise RuntimeError('Log channel is not available.')

		message_count = 0

		async for message in channel.history(limit=None, oldest_first=True):
			description = message.content if message.content else '*No text content*'
			embed = discord.Embed(
				title=message.author.display_name,
				color=discord.Color.blue(),
				description=description,
				timestamp=message.created_at,
			)
			await log_channel.send(embed=embed)

			for attachment in message.attachments:
				await log_channel.send(attachment.url)

			message_count += 1

		return message_count

	@app_commands.command(description='Purge channel (admin only)')
	@app_commands.describe(channel='Which channel do you want to purge?')
	@app_commands.checks.has_any_role(*data.admin_roles)
	@app_commands.guild_only()
	async def channelpurge(self, interaction: discord.Interaction, channel: discord.TextChannel | None) -> None:
		target_channel = self._resolve_text_channel(interaction, channel)
		if not self._is_temp_channel(target_channel):
			await send_ephemeral(interaction, embed=error_embed('Invalid channel.'))
			return

		await defer_response(interaction, ephemeral=True)

		deleted_messages = await target_channel.purge(
			limit=None,
			bulk=True,
			reason=f'Channel purge requested by {interaction.user}',
		)

		await send_ephemeral(
			interaction,
			embed=success_embed(f'Channel {target_channel.mention} purged ({len(deleted_messages)} messages deleted).'),
		)

	@app_commands.command(
		description='Creates a temp. private channel and invites the specified user to it (admin only)'
	)
	@app_commands.describe(member='Who do you want to invite?')
	@app_commands.checks.has_any_role(*data.admin_roles)
	@app_commands.guild_only()
	async def channelcreate(self, interaction: discord.Interaction, member: discord.Member) -> None:
		if interaction.guild is None:
			await send_ephemeral(interaction, embed=error_embed('Invalid guild.'))
			return

		guild = interaction.guild
		category = self.bot.get_channel(int(config.privcat))
		if category is not None and not isinstance(category, discord.CategoryChannel):
			category = None

		overwrites: dict[discord.Role | discord.Member, discord.PermissionOverwrite] = {
			guild.default_role: discord.PermissionOverwrite(view_channel=False),
			member: discord.PermissionOverwrite(view_channel=True),
		}

		bot_member = guild.me
		if bot_member is None and self.bot.user is not None:
			bot_member = guild.get_member(self.bot.user.id)

		if bot_member is not None:
			overwrites[bot_member] = discord.PermissionOverwrite(view_channel=True)

		for role_name in data.admin_roles:
			role = discord.utils.get(guild.roles, name=role_name)
			if role is not None:
				overwrites[role] = discord.PermissionOverwrite(view_channel=True)

		channel_name = f'temp_{member.name}'[:100]
		channel = await guild.create_text_channel(channel_name, overwrites=overwrites, category=category)
		await channel.send(f'This channel was created to discuss the private request of {member.mention}')

		await send_ephemeral(
			interaction,
			embed=success_embed(f'Channel {channel.mention} has been created for {member.mention}.'),
		)

	@app_commands.command(description='Copies the specified temp. channel to the archive (admin only)')
	@app_commands.describe(channel='Where do you want to copy things from?')
	@app_commands.checks.has_any_role(*data.admin_roles)
	@app_commands.guild_only()
	async def channelcopy(self, interaction: discord.Interaction, channel: discord.TextChannel | None) -> None:
		target_channel = self._resolve_text_channel(interaction, channel)
		if not self._is_temp_channel(target_channel):
			await send_ephemeral(interaction, embed=error_embed('Invalid channel.'))
			return

		await defer_response(interaction, ephemeral=True)

		try:
			archived_count = await self._archive_channel(target_channel)
		except RuntimeError:
			await send_ephemeral(interaction, embed=error_embed('Could not resolve archive channel.'))
			return

		await send_ephemeral(
			interaction,
			embed=success_embed(f'Messages have been archived ({archived_count} messages copied).'),
		)

	@app_commands.command(description='Copies the specified temp. channel to the archive and deletes it (admin only)')
	@app_commands.describe(channel='Which channel do you want to delete?')
	@app_commands.checks.has_any_role(*data.admin_roles)
	@app_commands.guild_only()
	async def channelkill(self, interaction: discord.Interaction, channel: discord.TextChannel | None) -> None:
		target_channel = self._resolve_text_channel(interaction, channel)
		if not self._is_temp_channel(target_channel):
			await send_ephemeral(interaction, embed=error_embed('Invalid channel.'))
			return

		await defer_response(interaction, ephemeral=True)

		try:
			archived_count = await self._archive_channel(target_channel)
		except RuntimeError:
			await send_ephemeral(interaction, embed=error_embed('Could not resolve archive channel.'))
			return

		await target_channel.delete(reason=f'Channel kill requested by {interaction.user}')

		await send_ephemeral(
			interaction,
			embed=success_embed(
				f'Messages have been archived ({archived_count} messages copied) and the channel deleted.'
			),
		)
