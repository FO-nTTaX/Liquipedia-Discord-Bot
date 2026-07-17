#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Callable

import discord
from discord import ui


IMAGE_PREVIEW_LIMIT = 4
FILE_LIST_LIMIT = 6

# Discord timeouts have a maximum duration close to 28 days.
# Due network latency the exact 28 days might not work and therefore its better to just set it to 27 days
TIMEOUT_DURATIONS: dict[str, tuple[timedelta, str]] = {
	'1h': (timedelta(hours=1), '1 hour'),
	'24h': (timedelta(hours=24), '24 hours'),
	'7d': (timedelta(days=7), '7 days'),
	'14d': (timedelta(days=14), '14 days'),
	'27d': (timedelta(days=27), '27 days'),
}

TIMEOUT_SELECT_OPTIONS = [
	discord.SelectOption(
		label=label,
		value=value,
		emoji='⏳',
	)
	for value, (_, label) in TIMEOUT_DURATIONS.items()
]


def truncate(text: str, limit: int) -> str:
	if len(text) <= limit:
		return text
	return text[: limit - 1].rstrip() + '…'


def quote_block(text: str, limit: int = 1024) -> str:
	if not text or not text.strip():
		return '*No text content*'
	return truncate('> ' + text.replace('\n', '\n> '), limit)


def copy_embeds(embeds: list[discord.Embed]) -> list[discord.Embed]:
	return [discord.Embed.from_dict(embed.to_dict()) for embed in embeds]


def display_name(user: discord.abc.User) -> str:
	return getattr(user, 'display_name', str(user))


def channel_label(channel: object) -> str:
	if hasattr(channel, 'name'):
		return '#' + getattr(channel, 'name')
	return str(channel)


def channel_mention(channel: object) -> str:
	return getattr(channel, 'mention', str(channel))


def is_image_attachment(attachment: discord.Attachment) -> bool:
	image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.avif', '.heic')

	if attachment.content_type is not None:
		return attachment.content_type.startswith('image/')
	return attachment.filename.casefold().endswith(image_extensions)


def escape_link_text(text: str) -> str:
	return text.replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]')


def files_value(attachments: list[discord.Attachment]) -> str:
	if not attachments:
		return ''

	lines = []
	for attachment in attachments[:FILE_LIST_LIMIT]:
		filename = escape_link_text(attachment.filename)
		lines.append(f'• [{filename}]({attachment.url})')

	if len(attachments) > FILE_LIST_LIMIT:
		lines.append(f'• +{len(attachments) - FILE_LIST_LIMIT} more file(s)')

	return truncate('\n'.join(lines), 1024)


def build_moderation_report_embeds(
	*,
	message: discord.Message,
	title: str,
	colour: discord.Colour,
	detail_name: str,
	detail_value: str,
	reporter_value: str,
) -> list[discord.Embed]:
	message_content = message.clean_content or message.system_content or ''
	channel_name = channel_label(message.channel)
	channel_ref = channel_mention(message.channel)

	image_attachments = [attachment for attachment in message.attachments if is_image_attachment(attachment)]
	non_image_attachments = [attachment for attachment in message.attachments if not is_image_attachment(attachment)]

	main_embed = discord.Embed(
		title=title,
		url=message.jump_url,
		colour=colour,
		timestamp=message.created_at,
	)

	main_embed.set_author(
		name=f'{display_name(message.author)} • {channel_name}',
		icon_url=message.author.display_avatar.url,
	)

	main_embed.add_field(
		name='Message',
		value=quote_block(message_content),
		inline=False,
	)
	main_embed.add_field(
		name=detail_name,
		value=quote_block(detail_value),
		inline=False,
	)
	main_embed.add_field(
		name='Reporter',
		value=reporter_value,
		inline=True,
	)
	main_embed.add_field(
		name='Author',
		value=message.author.mention,
		inline=True,
	)
	main_embed.add_field(
		name='Source',
		value=f'{channel_ref}\n{discord.utils.format_dt(message.created_at, style="f")}',
		inline=True,
	)

	author = message.author
	created_value = discord.utils.format_dt(author.created_at, style='R')

	main_embed.add_field(
		name='Account Age',
		value=created_value,
		inline=True,
	)

	if isinstance(author, discord.Member):
		joined_value = discord.utils.format_dt(author.joined_at, style='R') if author.joined_at else 'Unknown'
		main_embed.add_field(
			name='Joined Server',
			value=joined_value,
			inline=True,
		)
	else:
		main_embed.add_field(
			name='Status',
			value='Left Server / Unknown',
			inline=True,
		)

	files = files_value(non_image_attachments)
	if files:
		main_embed.add_field(
			name='Files',
			value=files,
			inline=False,
		)

	extra_image_count = max(0, len(image_attachments) - IMAGE_PREVIEW_LIMIT)
	if extra_image_count > 0:
		image_word = 'image' if extra_image_count == 1 else 'images'
		main_embed.add_field(
			name='Images',
			value=f'+{extra_image_count} more {image_word} on source message',
			inline=False,
		)

	embeds = [main_embed]

	if len(image_attachments) == 1:
		main_embed.set_image(url=image_attachments[0].url)
	elif len(image_attachments) > 1:
		for attachment in image_attachments[:IMAGE_PREVIEW_LIMIT]:
			image_embed = discord.Embed(url=message.jump_url)
			image_embed.set_image(url=attachment.url)
			embeds.append(image_embed)

	return embeds


def upsert_resolution_field(embed: discord.Embed, value: str) -> None:
	for index, field in enumerate(embed.fields):
		if field.name == 'Resolution':
			embed.set_field_at(index, name='Resolution', value=value, inline=False)
			return

	embed.insert_field_at(0, name='Resolution', value=value, inline=False)


class BaseResolutionView(ui.View):
	def __init__(self) -> None:
		# No permission checks because the report channel is admin-only.
		# Buttons on existing report messages will stop working if the bot restarts.
		super().__init__(timeout=None)
		self._action_lock = asyncio.Lock()
		self._handled = False
		self._in_progress = False

	async def _send_ephemeral(self, interaction: discord.Interaction, message: str) -> None:
		if interaction.response.is_done():
			await interaction.followup.send(message, ephemeral=True)
		else:
			await interaction.response.send_message(message, ephemeral=True)

	async def _begin_action(self, interaction: discord.Interaction) -> bool:
		reply: str | None = None

		async with self._action_lock:
			if self._handled:
				reply = 'This report has already been handled.'
			elif self._in_progress:
				reply = 'This report is already being handled by someone else.'
			else:
				self._in_progress = True
				return True

		if reply is not None:
			await self._send_ephemeral(interaction, reply)

		return False

	async def _start_action(self, interaction: discord.Interaction) -> bool:
		"""Lock the report and acknowledge the Discord button interaction immediately."""
		if not await self._begin_action(interaction):
			return False

		try:
			await interaction.response.defer()
		except discord.HTTPException:
			await self._cancel_action()
			await self._send_ephemeral(interaction, 'Could not start this moderation action.')
			return False

		return True

	async def _cancel_action(self) -> None:
		async with self._action_lock:
			if not self._handled:
				self._in_progress = False

	async def _fail_action(self, interaction: discord.Interaction, message: str) -> None:
		await self._cancel_action()
		await self._send_ephemeral(interaction, message)

	async def _mark_handled(self) -> None:
		async with self._action_lock:
			self._handled = True
			self._in_progress = False

	async def on_error(self, interaction: discord.Interaction, error: Exception, item) -> None:
		await self._cancel_action()

		if interaction.response.is_done():
			await interaction.followup.send('Something went wrong while processing this action.', ephemeral=True)
		else:
			await interaction.response.send_message(
				'Something went wrong while processing this action.',
				ephemeral=True,
			)

		raise error

	async def _finish(
		self,
		interaction: discord.Interaction,
		*,
		title: str,
		colour: discord.Colour,
		results: list[str],
		reaction_emoji: str | None = None,
		next_view: ui.View | None = None,
	) -> None:
		if interaction.message is None:
			await self._mark_handled()
			await self._send_ephemeral(
				interaction,
				'Moderation action completed, but the report message is no longer available to update.',
			)
			self.stop()
			return

		embeds = copy_embeds(list(interaction.message.embeds)) or [discord.Embed()]
		main_embed = embeds[0]
		main_embed.title = title
		main_embed.colour = colour
		upsert_resolution_field(main_embed, truncate('\n'.join(results), 1024))

		# Mark it handled before editing the report message so another click cannot
		# start the same action while Discord processes the message edit.
		await self._mark_handled()

		try:
			await interaction.message.edit(embeds=embeds, view=next_view)
		except (discord.Forbidden, discord.HTTPException, discord.NotFound):
			await self._send_ephemeral(
				interaction,
				'Moderation action completed, but the report message could not be updated.',
			)

		if reaction_emoji is not None:
			try:
				await interaction.message.add_reaction(reaction_emoji)
			except (discord.Forbidden, discord.HTTPException, discord.NotFound):
				pass

		self.stop()


class UnmuteView(BaseResolutionView):
	def __init__(self, target_member: discord.Member):
		super().__init__()
		self.target_member = target_member

	@ui.button(
		label='Unmute',
		emoji='🔊',
		style=discord.ButtonStyle.success,
	)
	async def unmute_user(self, interaction: discord.Interaction, button: ui.Button) -> None:
		if not await self._start_action(interaction):
			return

		try:
			await self.target_member.timeout(None, reason=f'Unmuted via report by {interaction.user}')
		except discord.Forbidden:
			await self._fail_action(interaction, 'Could not unmute user: missing permissions.')
			return
		except discord.HTTPException:
			await self._fail_action(interaction, 'Could not unmute user due to a Discord API error.')
			return

		await self._finish(
			interaction,
			title=f'Unmuted by {display_name(interaction.user)}',
			colour=discord.Colour.green(),
			results=[
				'User was timed out.',
				'**User unmuted.**',
			],
			reaction_emoji='🔊',
		)


class ReportActions(BaseResolutionView):
	def __init__(
		self,
		target_message: discord.Message,
		reporter_id: int,
		report_reason: str,
		on_report_resolved: Callable[[int], None] | None = None,
	):
		super().__init__()
		self.target_message = target_message
		self.reporter_id = reporter_id
		self.report_reason = report_reason
		self.on_report_resolved = on_report_resolved

	def _get_target_member(self, guild: discord.Guild | None) -> discord.Member | None:
		if guild is None:
			return None
		return guild.get_member(self.target_message.author.id)

	def _audit_reason(self, moderator: discord.abc.User, action: str) -> str:
		compact_reason = ' '.join(self.report_reason.split())
		compact_reason = truncate(compact_reason, 200)

		return (
			f'{action} via report by {moderator} | '
			f'reporter_id={self.reporter_id} | '
			f'message_id={self.target_message.id} | '
			f'reason={compact_reason}'
		)

	async def _delete_reported_message(self) -> tuple[str, str]:
		try:
			await self.target_message.delete()
			return ('Reported message deleted.', 'deleted')
		except discord.NotFound:
			return ('Reported message was already deleted.', 'already_deleted')
		except discord.Forbidden:
			return ('Could not delete the reported message: missing permissions.', 'failed')
		except discord.HTTPException:
			return ('Could not delete the reported message due to a Discord API error.', 'failed')

	async def _apply_timeout(
		self,
		interaction: discord.Interaction,
		*,
		duration: timedelta,
		duration_label: str,
	) -> None:
		if not await self._start_action(interaction):
			return

		if interaction.guild is None:
			await self._fail_action(interaction, 'This action can only be used inside a server.')
			return

		member = self._get_target_member(interaction.guild)
		if member is None:
			await self._fail_action(
				interaction,
				'Could not timeout user: they are no longer in the server.',
			)
			return

		try:
			await member.timeout(
				duration,
				reason=self._audit_reason(
					interaction.user,
					f'Timeout for {duration_label}',
				),
			)
		except discord.Forbidden:
			await self._fail_action(
				interaction,
				'Could not timeout user: missing permissions or role hierarchy.',
			)
			return
		except discord.HTTPException:
			await self._fail_action(
				interaction,
				'Could not timeout user due to a Discord API error.',
			)
			return

		results = [f'User timed out for {duration_label}.']
		delete_result, _ = await self._delete_reported_message()
		results.append(delete_result)

		if self.on_report_resolved is not None:
			self.on_report_resolved(self.target_message.author.id)

		await self._finish(
			interaction,
			title=f'Timed out for {duration_label} by {display_name(interaction.user)}',
			colour=discord.Colour.orange(),
			results=results,
			reaction_emoji='⏳',
			next_view=UnmuteView(member),
		)

	@ui.button(
		label='Ban',
		emoji='🔨',
		style=discord.ButtonStyle.danger,
		row=0,
	)
	async def ban_user(self, interaction: discord.Interaction, button: ui.Button) -> None:
		if not await self._start_action(interaction):
			return

		if interaction.guild is None:
			await self._fail_action(interaction, 'This action can only be used inside a server.')
			return

		try:
			await interaction.guild.ban(
				self.target_message.author,
				reason=self._audit_reason(interaction.user, 'Ban'),
				delete_message_seconds=86400,
			)
		except discord.Forbidden:
			await self._fail_action(
				interaction,
				'Could not ban user: missing permissions or role hierarchy.',
			)
			return
		except discord.HTTPException:
			await self._fail_action(
				interaction,
				'Could not ban user due to a Discord API error.',
			)
			return

		results = ['User banned.']
		delete_result, _ = await self._delete_reported_message()
		results.append(delete_result)

		if self.on_report_resolved is not None:
			self.on_report_resolved(self.target_message.author.id)

		await self._finish(
			interaction,
			title=f'Banned by {display_name(interaction.user)}',
			colour=discord.Colour.red(),
			results=results,
			reaction_emoji='🔨',
		)

	@ui.select(
		placeholder='Timeout duration…',
		min_values=1,
		max_values=1,
		options=TIMEOUT_SELECT_OPTIONS,
		row=1,
	)
	async def apply_timeout(
		self,
		interaction: discord.Interaction,
		select: ui.Select,
	) -> None:
		timeout_choice = select.values[0]
		timeout = TIMEOUT_DURATIONS.get(timeout_choice)

		if timeout is None:
			await self._send_ephemeral(interaction, 'Invalid timeout duration selected.')
			return

		duration, duration_label = timeout
		await self._apply_timeout(
			interaction,
			duration=duration,
			duration_label=duration_label,
		)

	@ui.button(
		label='Delete',
		emoji='🗑️',
		style=discord.ButtonStyle.danger,
		row=0,
	)
	async def delete_message(self, interaction: discord.Interaction, button: ui.Button) -> None:
		if not await self._start_action(interaction):
			return

		delete_result, delete_status = await self._delete_reported_message()

		if delete_status == 'failed':
			await self._fail_action(interaction, delete_result)
			return

		if self.on_report_resolved is not None:
			self.on_report_resolved(self.target_message.author.id)

		await self._finish(
			interaction,
			title=f'Deleted by {display_name(interaction.user)}',
			colour=discord.Colour.blue(),
			results=[delete_result],
			reaction_emoji='🗑️',
		)

	@ui.button(
		label='Dismiss',
		emoji='✅',
		style=discord.ButtonStyle.secondary,
		row=0,
	)
	async def dismiss_report(self, interaction: discord.Interaction, button: ui.Button) -> None:
		if not await self._start_action(interaction):
			return

		if self.on_report_resolved is not None:
			self.on_report_resolved(self.target_message.author.id)

		await self._finish(
			interaction,
			title=f'Dismissed by {display_name(interaction.user)}',
			colour=discord.Colour.green(),
			results=['No moderation action taken.'],
			reaction_emoji='✅',
		)


class AntispamActions(BaseResolutionView):
	def __init__(
		self,
		*,
		target_member_id: int,
		guild_id: int,
		message_content: str,
		on_report_resolved: Callable[[int], None] | None = None,
	):
		super().__init__()
		self.target_member_id = target_member_id
		self.guild_id = guild_id
		self.message_content = message_content
		self.on_report_resolved = on_report_resolved

	def _guild(self, interaction: discord.Interaction) -> discord.Guild | None:
		return interaction.client.get_guild(self.guild_id)

	@ui.button(
		label='Ban',
		emoji='🔨',
		style=discord.ButtonStyle.danger,
	)
	async def ban_user(self, interaction: discord.Interaction, button: ui.Button) -> None:
		if not await self._start_action(interaction):
			return

		guild = self._guild(interaction)
		if guild is None:
			await self._fail_action(interaction, 'Could not find server.')
			return

		try:
			await guild.ban(
				discord.Object(id=self.target_member_id),
				reason=f'Automated anti-spam ban confirmed by {interaction.user}',
				delete_message_seconds=0,
			)
		except discord.Forbidden:
			await self._fail_action(interaction, 'Could not ban user: missing permissions.')
			return
		except discord.HTTPException:
			await self._fail_action(interaction, 'Could not ban user due to a Discord API error.')
			return

		if self.on_report_resolved is not None:
			self.on_report_resolved(self.target_member_id)

		await self._finish(
			interaction,
			title=f'Banned by {display_name(interaction.user)}',
			colour=discord.Colour.red(),
			results=['Automod timeout confirmed and escalated to ban.'],
			reaction_emoji='🔨',
		)

	@ui.button(
		label='Unmute',
		emoji='🔊',
		style=discord.ButtonStyle.success,
	)
	async def unmute_user(self, interaction: discord.Interaction, button: ui.Button) -> None:
		if not await self._start_action(interaction):
			return

		guild = self._guild(interaction)
		member = guild.get_member(self.target_member_id) if guild else None

		if member is None:
			await self._fail_action(
				interaction,
				'Could not find user in the server (they may have left).',
			)
			return

		try:
			await member.timeout(None, reason=f'Automated anti-spam timeout reverted by {interaction.user}')
		except discord.Forbidden:
			await self._fail_action(interaction, 'Could not unmute user: missing permissions.')
			return
		except discord.HTTPException:
			await self._fail_action(interaction, 'Could not unmute user due to a Discord API error.')
			return

		if self.on_report_resolved is not None:
			self.on_report_resolved(self.target_member_id)

		await self._finish(
			interaction,
			title=f'Unmuted by {display_name(interaction.user)}',
			colour=discord.Colour.green(),
			results=['Automod timeout reverted.'],
			reaction_emoji='🔊',
		)

	@ui.button(
		label='Get Raw Text',
		emoji='📋',
		style=discord.ButtonStyle.secondary,
	)
	async def get_raw_text(self, interaction: discord.Interaction, button: ui.Button) -> None:
		if not self.message_content:
			await interaction.response.send_message('No message content to copy.', ephemeral=True)
			return

		safe_text = self.message_content.replace('`', '`\u200b')
		if len(safe_text) > 1900:
			safe_text = safe_text[:1900] + '... (truncated)'

		await interaction.response.send_message(f'```\n{safe_text}\n```', ephemeral=True)

	@ui.button(
		label='Dismiss',
		emoji='✅',
		style=discord.ButtonStyle.secondary,
	)
	async def dismiss(self, interaction: discord.Interaction, button: ui.Button) -> None:
		if not await self._start_action(interaction):
			return

		if self.on_report_resolved is not None:
			self.on_report_resolved(self.target_member_id)

		await self._finish(
			interaction,
			title=f'Dismissed by {display_name(interaction.user)}',
			colour=discord.Colour.light_grey(),
			results=['Automod action kept. No further moderator action taken.'],
			reaction_emoji='✅',
		)
