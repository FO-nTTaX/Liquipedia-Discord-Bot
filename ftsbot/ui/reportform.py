#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 4.1.1

from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import ui

from ftsbot import config

if TYPE_CHECKING:
	from ftsbot.liquipediabot import LiquipediaBot


class ReportForm(ui.Modal, title='Report message to LP Admins'):
	whatswrong = ui.TextInput(label='What is wrong with this message', style=discord.TextStyle.paragraph)

	def __init__(self, bot: LiquipediaBot, message: discord.Message):
		super().__init__()
		self.bot = bot
		self.message = message

	@staticmethod
	def format_quote(message: str) -> str:
		if not message:
			return '> '
		return '> ' + message.replace('\n', '\n> ')

	async def on_submit(self, interaction: discord.Interaction) -> None:
		report_channel = self.bot.get_channel(config.reporttarget)
		if not isinstance(report_channel, discord.TextChannel):
			await interaction.response.send_message(
				'Could not send your report right now. Please try again later.',
				ephemeral=True,
			)
			return

		message_content = self.message.clean_content or 'No text content'
		await report_channel.send(
			embed=discord.Embed(
				colour=discord.Colour.red(),
				title='A message has been reported',
				description=(
					f'Message content:\n{self.format_quote(message_content)}\n\n'
					f'Report reason by {interaction.user.mention}:\n'
					f'{self.format_quote(self.whatswrong.value)}\n\n'
					f'User {self.message.author.mention} in {self.message.jump_url}'
				),
			)
		)

		await interaction.response.send_message(
			'Thank you for your report, it has been sent to the Liquipedia Administrators.',
			ephemeral=True,
		)
