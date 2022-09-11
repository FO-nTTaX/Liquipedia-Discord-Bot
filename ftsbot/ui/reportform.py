#!/usr/bin/env python3

# License MIT
# Copyright 2016-2022 Alex Winkler
# Version 4.0.0

import discord
from discord import ui
from ftsbot import config

class reportform(ui.Modal, title='Report message to LP Admins'):
	def __init__(self, bot, message):
		self.bot = bot
		self.message = message
		super().__init__()

	whatswrong = ui.TextInput(label='What is wrong with this message?', style=discord.TextStyle.paragraph)

	async def on_submit(self, interaction: discord.Interaction):
		await interaction.response.send_message('Thank you for your report, it has been sent to the Liquipedia Administrators', ephemeral=True)

		reporttarget = self.bot.get_channel(config.reporttarget)
		text = interaction.user.mention + '** has reported this message:**\n\n' + self.message.jump_url + ' by ' + self.message.author.mention + ' with the following content:\n\n' + self.formatquote(self.message.clean_content) + '\n\n**The following reason has been given:**\n\n' + self.formatquote(self.whatswrong.value)
		await reporttarget.send(text)

	def formatquote(self, message):
		return '> ' + message.replace('\n', '\n> ')
