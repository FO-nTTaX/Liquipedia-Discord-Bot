#!/usr/bin/env python3

# License MIT
# Copyright 2016-2023 Alex Winkler
# Version 4.0.3

import discord
from discord import ui
from ftsbot import config


class reportform(
	ui.Modal,
	title='Report message to LP Admins'
):
	def __init__(
		self,
		bot,
		message
	):
		self.bot = bot
		self.message = message
		super().__init__()

	whatswrong = ui.TextInput(
		label='What is wrong with this message?',
		style=discord.TextStyle.paragraph
	)

	async def on_submit(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			'Thank you for your report, it has been sent to the Liquipedia Administrators',
			ephemeral=True
		)

		reporttarget = self.bot.get_channel(config.reporttarget)
		await reporttarget.send(
			embed=discord.Embed(
				colour=discord.Colour.red(),
				title=(
					'A message has been reported'
				),
				description=(
					'Message content:\n' + self.formatquote(self.message.clean_content)
					+ '\n\nReport reason by :' interaction.user.mention
					+ '\n' + self.formatquote(self.whatswrong.value)
					+ '\n\nUser: ' + self.message.author.mention + ' in ' + self.message.jump_url
				)
			)
		)

	def formatquote(
		self,
		message
	):
		return '> ' + message.replace('\n', '\n> ')
