#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

from __future__ import annotations

from typing import Callable

import discord
from discord import ui

from ftsbot import config
from ftsbot.ui.moderation_views import ReportActions, build_moderation_report_embeds


class ReportForm(ui.Modal, title='Report message to LP Admins'):
	whatswrong = ui.TextInput(
		label='What is wrong with this message?',
		style=discord.TextStyle.paragraph,
		placeholder='Briefly explain the issue.',
		max_length=248,
		required=True,
	)

	def __init__(
		self,
		bot,
		message: discord.Message,
		on_report_sent: Callable[[int], None] | None = None,
		on_report_resolved: Callable[[int], None] | None = None,
	):
		self.bot = bot
		self.message = message
		self.on_report_sent = on_report_sent
		self.on_report_resolved = on_report_resolved
		super().__init__()

	def _build_embeds(self, interaction: discord.Interaction) -> list[discord.Embed]:
		return build_moderation_report_embeds(
			message=self.message,
			title='Reported message',
			colour=discord.Colour.red(),
			detail_name='Reason',
			detail_value=self.whatswrong.value,
			reporter_value=interaction.user.mention,
		)

	async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
		if interaction.response.is_done():
			await interaction.followup.send('Something went wrong while submitting the report.', ephemeral=True)
		else:
			await interaction.response.send_message('Something went wrong while submitting the report.', ephemeral=True)
		raise error

	async def on_submit(self, interaction: discord.Interaction):
		if self.message.guild is None:
			await interaction.response.send_message(
				'Reporting messages sent via Direct Messages is not allowed. This tool is only for server messages.',
				ephemeral=True,
			)
			return

		reporttarget = self.bot.get_channel(config.reporttarget)
		if not isinstance(reporttarget, discord.TextChannel):
			await interaction.response.send_message(
				'Could not send your report right now. Please try again later.',
				ephemeral=True,
			)
			return

		view = ReportActions(
			target_message=self.message,
			reporter_id=interaction.user.id,
			report_reason=self.whatswrong.value,
			on_report_resolved=self.on_report_resolved,
		)

		try:
			await reporttarget.send(
				embeds=self._build_embeds(interaction),
				view=view,
			)
		except discord.HTTPException:
			await interaction.response.send_message(
				'Could not send your report right now. Please try again later.',
				ephemeral=True,
			)
			return

		if self.on_report_sent is not None:
			self.on_report_sent(self.message.author.id)

		await interaction.response.send_message(
			'Thank you for your report, it has been sent to the Liquipedia Administrators.',
			ephemeral=True,
		)
