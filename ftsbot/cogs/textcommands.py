#!/usr/bin/env python3

# License MIT
# Copyright 2016-2023 Alex Winkler
# Version 4.0.3

import discord
from discord import app_commands
from discord.ext import commands
from ftsbot import config, data
from ftsbot.functions import autocomplete
import random
import typing


class textcommands(
	commands.Cog
):
	def __init__(
		self,
		bot
	):
		self.bot = bot

	@app_commands.command(
		description='Author information'
	)
	@app_commands.checks.cooldown(
		1,
		300,
		key=lambda i: (i.guild_id, i.user.id)
	)
	async def author(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x663399),
				description='FO-BoT was coded by **FO-nTTaX**'
			)
		)

	@author.error
	async def on_author_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError
	):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)

	@app_commands.command(
		description='On shady betting sites'
	)
	async def betting(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x00ffff),
				description='[On shady betting sites](https://liquipedia.net/commons/User:FO-nTTaX/Betting)'
			)
		)

	@app_commands.command(
		description='Blame someone'
	)
	@app_commands.checks.cooldown(
		1,
		300,
		key=lambda i: (i.guild_id, i.user.id)
	)
	async def blame(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x663399),
				description='**#blamesalle**'
			)
		)

	@blame.error
	async def on_blame_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError
	):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)

	@app_commands.command(
		description='Dance'
	)
	@app_commands.checks.cooldown(
		1,
		300,
		key=lambda i: (i.guild_id, i.user.id)
	)
	async def dance(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x663399),
				description='**EVERYBODY DANCE \\\\Ü/**\n*dances :D\\\\-<*\n*dances :D|-<*\n*dances :D/-<*'
			)
		)

	@dance.error
	async def on_dance_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError
	):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)

	@app_commands.command(
		description='Roll a die'
	)
	@app_commands.describe(
		sides='How many sides (default 6)?',
		amount='How many dice (default 1)?',
	)
	@app_commands.checks.cooldown(
		1,
		300,
		key=lambda i: (i.guild_id, i.user.id)
	)
	async def dice(
		self,
		interaction: discord.Interaction,
		sides: typing.Optional[int] = 6,
		amount: typing.Optional[int] = 1
	):
		if sides < 2:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='A die needs to have a least 2 sides'
				)
			)
		elif amount < 1:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='You need to roll at least one die'
				)
			)
		result = ''
		if amount == 1:
			result = 'Your ' + str(sides) + '-sided die threw a ' + str(random.randrange(1, sides + 1, 1)) + '.'
		else:
			rolls = [random.randrange(1, sides + 1, 1) for _ in range(amount)]
			result = (
				'Your '
				+ str(amount)
				+ ' '
				+ str(sides)
				+ '-sided dice threw '
				+ str(rolls)
				+ ' for a total of '
				+ str(sum(rolls))
				+ '.'
			)
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x663399),
				description=result
			)
		)

	@dice.error
	async def on_dice_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError
	):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)

	@app_commands.command(
		description='Links to guides'
	)
	@app_commands.checks.cooldown(
		1,
		300,
		key=lambda i: (i.guild_id, i.user.id)
	)
	async def guides(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x00ffff),
				description='**Liquipedia-Guides**: https://liquipedia.net/starcraft2/User:FO-BoT#Guides'
			)
		)

	@guides.error
	async def on_guides_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError
	):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)

	@app_commands.command(
		description='\\Ü/ HYPE \\Ü/'
	)
	@app_commands.checks.cooldown(
		1,
		300,
		key=lambda i: (i.guild_id, i.user.id)
	)
	async def hype(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x663399),
				description='**\\\\Ü/ HYPE \\\\Ü/**'
			)
		)
		await interaction.response.send_message('https://i.imgur.com/xmdBFq9.mp4')

	@hype.error
	async def on_hype_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError
	):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)

	@app_commands.command(
		description='Tell people to just ask!'
	)
	async def justask(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x00ffff),
				description=(
					'If you need help with something or just have a question, please post the question in the channel '
					+ 'for the relevant wiki.'
					+ ' Asking if someone can help only costs you extra time, and you usually don\'t even need an admin!'
				)
			)
		)

	@app_commands.command(
		description='Tell people the minimum requirements for admin requests!'
	)
	async def adminrequestrequirements(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x00ffff),
				title=('What are the minimum requirements for any admin requests?'),
				description=(
					'__What are the minimum requirements for any admin requests?__\n'
					+ '- provide an explanation what should be done\n'
					+ '- be as precise as possible and include links where possible\n'
					+ ' - for bans, it helps to link to contributions pages or edits that are ban worthy\n'
					+ ' - for changes on locked pages, link to the page that is to be changed\n'
					+ ' - for bot runs if, you know the exact command it is appreciated, if you do not '
					+ 'know it write down exactly what is to be done and on which wiki\n'
					+ '- explain why it should be done\n'
					+ ' - for changes on locked pages (e.g. css sheets), this includes specific examples '
					+ 'that get fixed/improved due to the change and if possible also a reasoning why it '
					+ 'doesn\'t break other stuff\n'
					+ ' - for bans, it includes the reasons why you think a ban is needed as well as an '
					+ 'example (a change they did that you think is ban-worthy)\n'
					+ '- be polite and patient instead of demanding, remember that admins help on liquipedia '
					+ 'voluntarily in their free time'
				)
			)
		)

	@app_commands.command(
		description='Lickypiddy!'
	)
	@app_commands.checks.cooldown(
		1,
		300,
		key=lambda i: (i.guild_id, i.user.id)
	)
	async def lickypiddy(
		self,
		interaction: discord.Interaction
	):
		lickypiddywiki = 'commons'
		if isinstance(interaction.channel, discord.channel.TextChannel) and interaction.channel.name in data.wikis:
			lickypiddywiki = interaction.channel.name
		else:
			lickypiddywiki = 'commons'
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x663399),
				description='[\\\\Ü/ All glory Lickypiddy \\\\Ü/](https://liquipedia.net/' + lickypiddywiki + '/Special:Lickypiddy)'
			)
		)

	@lickypiddy.error
	async def on_lickypiddy_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError
	):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)

	@app_commands.command(
		description='Tell a lie'
	)
	@app_commands.checks.cooldown(
		1,
		300,
		key=lambda i: (i.guild_id, i.user.id)
	)
	async def lie(
		self,
		interaction: discord.Interaction
	):
		i = random.randrange(0, len(data.lies), 1)
		response = data.lies[i]
		if response.startswith('http'):
			await interaction.response.send_message(response)
		else:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0x663399),
					description=response
				)
			)

	@lie.error
	async def on_lie_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError
	):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)

	@app_commands.command(
		description='Liquipedia!'
	)
	@app_commands.checks.cooldown(
		1,
		300,
		key=lambda i: (i.guild_id, i.user.id)
	)
	async def liquipedia(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x00ffff),
				description='**Liquipedia** is awesome!'
			)
		)

	@liquipedia.error
	async def on_liquipedia_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError
	):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)

	@app_commands.command(
		description='Link the notability guidelines!'
	)
	@app_commands.describe(
		wiki='Which wiki do you want the notability guidelines for?',
	)
	@app_commands.autocomplete(
		wiki=autocomplete.wiki
	)
	async def notability(
		self,
		interaction: discord.Interaction,
		wiki: typing.Optional[str]
	):
		usewiki = None
		if wiki in data.wikis:
			usewiki = wiki
		elif isinstance(interaction.channel, discord.channel.TextChannel) and interaction.channel.name in data.wikis:
			usewiki = interaction.channel.name
		if usewiki is not None:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0x00ff00),
					description='[Notability Guidelines](https://liquipedia.net/' + usewiki + '/Liquipedia:Notability_Guidelines)'
				)
			)
		else:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='No wiki specified'
				)
			)

	@app_commands.command(
		description='Edit Statistics'
	)
	@app_commands.checks.cooldown(
		1,
		300,
		key=lambda i: (i.guild_id, i.user.id)
	)
	async def ranking(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x00ffff),
				description='**Liquipedia ranking**: https://liquipedia.net/statistics/?view=editcount&wikilist=all'
			)
		)

	@ranking.error
	async def on_ranking_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError
	):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)

	@app_commands.command(
		description='Send a link to the request form'
	)
	async def request(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x00ffff),
				description='[Liquipedia Request Form](https://forms.gle/1zcZHkKe6udPNv2v6)'
			)
		)

	@app_commands.command(
		description='Think very hard'
	)
	@app_commands.checks.cooldown(
		1,
		300,
		key=lambda i: (i.guild_id, i.user.id)
	)
	async def thinking(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message('https://files.catbox.moe/o8tify.gif')

	@app_commands.command(
		description='Troll'
	)
	@app_commands.describe(
		channel='Which channel do you want to troll?',
		message='What do you want to send?',
	)
	@app_commands.guilds(
		discord.Object(id=config.commandserver)
	)
	async def troll(
		self,
		interaction: discord.Interaction,
		channel: str,
		message: str
	):
		targetchannel = discord.utils.get(discord.utils.get(self.bot.guilds, id=config.runserver).channels, name=channel)
		if targetchannel is None or not isinstance(targetchannel, discord.channel.TextChannel):
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='**Error**: Can only send messages to existing text channels'
				)
			)
		else:
			sent_message = await targetchannel.send(message)
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0x00ff00),
					description=(
						'**Channel**: ' + targetchannel.mention
						+ '\n**Link**: ' + sent_message.jump_url
						+ '\n**Message**: ' + message
					)
				)
			)

	@thinking.error
	async def on_thinking_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError
	):
		if isinstance(error, app_commands.CommandOnCooldown):
			await interaction.response.send_message(str(error), ephemeral=True)
