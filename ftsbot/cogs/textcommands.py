#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

from __future__ import annotations

import random
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from ftsbot import config, data
from ftsbot.functions import autocomplete
from ftsbot.utils.embeds import accent_embed, error_embed, info_embed
from ftsbot.utils.interactions import send_ephemeral

if TYPE_CHECKING:
	from ftsbot.liquipediabot import LiquipediaBot


class TextCommands(commands.Cog):
	MAX_DICE_AMOUNT = 100
	MAX_DICE_SIDES = 1_000_000

	def __init__(self, bot: LiquipediaBot):
		self.bot = bot

	async def _handle_cooldown_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError,
	) -> None:
		if isinstance(error, app_commands.CommandOnCooldown):
			await send_ephemeral(interaction, content=str(error))
			return

		raise error

	def _resolve_channel_wiki(self, interaction: discord.Interaction) -> str | None:
		if isinstance(interaction.channel, discord.TextChannel) and interaction.channel.name in data.wikis:
			return interaction.channel.name
		return None

	@app_commands.command(description='Author information')
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def author(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(embed=accent_embed('FO-BoT was coded by **FO-nTTaX**'))

	@author.error
	async def on_author_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='On shady betting sites')
	async def betting(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(
			embed=info_embed('[On shady betting sites](https://liquipedia.net/hub/Liquipedia:On_Shady_Betting_Sites)')
		)

	@app_commands.command(description='Blame someone')
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def blame(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(embed=accent_embed('**#blamesalle**'))

	@blame.error
	async def on_blame_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='Information about content removals')
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def contentremoval(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(
			embed=info_embed(
				'To have personal information removed from our wikis, please send an email to '
				'"contact@liquipedia.net" with an explanation of the request and any relevant links. '
				'For further information please refer to '
				'[our content removal policy](https://liquipedia.net/hub/Liquipedia:Policy#Removal_of_Content).'
			)
		)

	@contentremoval.error
	async def on_contentremoval_error(
		self, interaction: discord.Interaction, error: app_commands.AppCommandError
	) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='Dance')
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def dance(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(
			embed=accent_embed('**EVERYBODY DANCE \\\\Ü/**\n*dances :D\\\\-<*\n*dances :D|-<*\n*dances :D/-<*')
		)

	@dance.error
	async def on_dance_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='Roll a die')
	@app_commands.describe(
		sides='How many sides (default 6)?',
		amount='How many dice (default 1)?',
	)
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def dice(self, interaction: discord.Interaction, sides: int = 6, amount: int = 1) -> None:
		if sides < 2:
			await interaction.response.send_message(embed=error_embed('A die needs to have at least 2 sides.'))
			return

		if amount < 1:
			await interaction.response.send_message(embed=error_embed('You need to roll at least one die.'))
			return

		if sides > self.MAX_DICE_SIDES:
			await interaction.response.send_message(
				embed=error_embed(f'Dice can have at most {self.MAX_DICE_SIDES:,} sides.')
			)
			return

		if amount > self.MAX_DICE_AMOUNT:
			await interaction.response.send_message(
				embed=error_embed(f'You can roll at most {self.MAX_DICE_AMOUNT} dice at once.')
			)
			return

		if amount == 1:
			result = f'Your {sides}-sided die threw a {random.randrange(1, sides + 1)}.'
		else:
			rolls = [random.randrange(1, sides + 1) for _ in range(amount)]
			result = f'Your {amount} {sides}-sided dice threw {rolls} for a total of {sum(rolls)}.'

		await interaction.response.send_message(embed=accent_embed(result))

	@dice.error
	async def on_dice_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='Links to guides')
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def guides(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(
			embed=info_embed('**Liquipedia Support Hub**: https://liquipedia.net/hub/Support')
		)

	@guides.error
	async def on_guides_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='\\Ü/ HYPE \\Ü/')
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def hype(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(embed=accent_embed('**\\\\Ü/ HYPE \\\\Ü/**'))
		await interaction.followup.send('https://i.imgur.com/xmdBFq9.mp4')

	@hype.error
	async def on_hype_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='Tell people to just ask!')
	async def justask(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(
			embed=info_embed(
				'If you need help with something or just have a question, please post the question in the channel '
				'for the relevant wiki. Asking if someone can help only costs you extra time, and you usually do '
				'not even need an admin!'
			)
		)

	@app_commands.command(description='Tell people the minimum requirements for admin requests!')
	async def adminrequestrequirements(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(
			embed=info_embed(
				'__What are the minimum requirements for any admin requests?__\n'
				'- provide an explanation what should be done\n'
				'- be as precise as possible and include links when possible\n'
				' - for bans, it helps to link to contributions pages or edits that are ban worthy\n'
				' - for changes on locked pages, link to the page that needs to be changed\n'
				' - for bot runs, if you know the exact command it is appreciated, if you do not know it, write down '
				'exactly what should be changed and on which wiki\n'
				' - for page deletions, link the pages and explain why they should be deleted\n'
				'- explain why it should be done\n'
				' - for changes on locked pages (e.g. css sheets), include specific examples that will be '
				'fixed/improved due to the change and if possible also a reasoning why it does not break other stuff\n'
				' - for bans, include the reasons why you think a ban is needed as well as an example '
				'(a change they did that you think is ban-worthy)\n'
				'- be polite and patient instead of demanding, remember that admins help on Liquipedia voluntarily '
				'in their free time',
				title='What are the minimum requirements for any admin requests?',
			)
		)

	@app_commands.command(description='Inform someone as to why they could be getting rate limited!')
	async def ratelimited(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(
			embed=info_embed(
				'__What actions could result in being rate limited?__\n'
				'- using a scraper or similar bot\n'
				' - note that using a scraper is against the Liquipedia [terms of service](https://tl.net/tou/)\n'
				'breach of TOS can result in a ban\n'
				'- opening numerous pages in quick succession\n'
				' - older tournament pages have been known to trigger being rate limited more than other page types\n'
				'- your IP address is used by others\n'
				' - using a dynamic IP, this is when your IP address is continuously changed, potentially landing on '
				'an IP that is rate limited\n'
				' - using public wifi connections such as universities or internet cafes\n'
				' - multiple users on the same internet connection accessing pages in rapid succession\n'
				'- using browser extensions that cause unnecessary network requests or pre-fetching\n'
				'- corporate or school firewalls/content scanners\n'
				'- potential malware on your PC or network\n'
				'- being a residential proxy botnet member\n'
				'__Measures to prevent or resolve being rate limited__\n'
				'- discontinue any instances of aforementioned causes\n'
				'- get a static IP address\n'
				'- [check if your IP is used in a bot net](https://check.labs.greynoise.io/)\n'
				'- wait for a Liquipedia employee to assist you, note that your IP address may be requested, you will '
				'be helped at their earliest convenience\n'
				'- if none of the previous options work you should contact your internet service provider\n'
				'- if this is only your first time being rate limited you can complete the CAPTCHA to unblock yourself, '
				'being continuously rate limited can result in it becoming permanent',
				title='What actions could result in being rate limited?',
			)
		)

	@app_commands.command(description='Lickypiddy!')
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def lickypiddy(self, interaction: discord.Interaction) -> None:
		wiki = self._resolve_channel_wiki(interaction) or 'commons'
		# All glory Lickypiddy!
		await interaction.response.send_message(
			embed=accent_embed(
				f'[\\\\Ü/ All glory Lickypiddy \\\\Ü/](https://liquipedia.net/{wiki}/Special:Lickypiddy)'
			)
		)

	@lickypiddy.error
	async def on_lickypiddy_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='Tell a lie')
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def lie(self, interaction: discord.Interaction) -> None:
		response = random.choice(data.lies)
		if response.startswith('http'):
			await interaction.response.send_message(response)
			return

		await interaction.response.send_message(embed=accent_embed(response))

	@lie.error
	async def on_lie_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='Liquipedia!')
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def liquipedia(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(embed=info_embed('**Liquipedia** is awesome!'))

	@liquipedia.error
	async def on_liquipedia_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='Link the notability guidelines!')
	@app_commands.describe(
		wiki='Which wiki do you want the notability guidelines for?',
		user='Which user is the guidelines directed towards?',
	)
	@app_commands.autocomplete(wiki=autocomplete.wiki)
	async def notability(
		self,
		interaction: discord.Interaction,
		wiki: str | None,
		user: discord.User | None,
	) -> None:
		usewiki = wiki if wiki in data.wikis else self._resolve_channel_wiki(interaction)
		if usewiki is None:
			await send_ephemeral(interaction, embed=error_embed('No wiki specified.'))
			return

		if user is None:
			await interaction.response.send_message(
				embed=info_embed(
					f'[Notability Guidelines](https://liquipedia.net/{usewiki}/Liquipedia:Notability_Guidelines)'
				)
			)
			return

		await interaction.response.send_message(
			embed=info_embed(
				f'Hi {user.mention},\n\n'
				f'Please have a read of [this document](https://liquipedia.net/{usewiki}/Liquipedia:Notability_Guidelines) '
				'about page notability.\n\n'
				f"Almost all of {usewiki}'s day-to-day edits are made by volunteers. These guidelines are in place to "
				'make sure that they are not overwhelmed by the amount of pages that need to be kept up-to-date.\n\n'
				'If you think we have made a mistake while determining the notability of a player, organisation, or '
				'broadcast talent member, please let us know in this channel. Please include links to social media '
				'posts, news articles or your own materials when doing so!\n\n'
				f'Thanks,\n{interaction.user.name}'
			)
		)

	@app_commands.command(description='Help on how to submit a photo')
	@app_commands.describe(user='Which user is the guidelines directed towards?')
	async def photos(self, interaction: discord.Interaction, user: discord.User | None) -> None:
		if user is None:
			await interaction.response.send_message(
				embed=info_embed(
					'Please have the copyright owner email the image to "photos@liquipedia.net", alongside a '
					'statement giving their permission for it to be used on Liquipedia. Please also include what '
					'wiki the image is for and the player in question.'
				)
			)
			return

		await interaction.response.send_message(
			embed=info_embed(
				f'Hi {user.mention},\n\n'
				'Due to copyright law we cannot include photos without permission from their owner. Often this will '
				'be either the photographer themself or the organizer of the event.\n\n'
				'Please have the copyright owner email the image to "photos@liquipedia.net", alongside a statement '
				'giving their permission for it to be used on Liquipedia. Please also include what wiki the image is '
				'for and the player in question.\n\n'
				f'Thanks,\n{interaction.user.name}'
			)
		)

	@app_commands.command(description='Edit Statistics')
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def ranking(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(
			embed=info_embed('**Liquipedia ranking**: https://liquipedia.net/statistics/?view=editcount&wikilist=all')
		)

	@ranking.error
	async def on_ranking_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='Think very hard')
	@app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
	async def thinking(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message('https://files.catbox.moe/o8tify.gif')

	@thinking.error
	async def on_thinking_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		await self._handle_cooldown_error(interaction, error)

	@app_commands.command(description='Troll')
	@app_commands.describe(
		channel='Which channel do you want to troll?',
		message='What do you want to send?',
	)
	@app_commands.guilds(discord.Object(id=config.commandserver))
	@app_commands.guild_only()
	async def troll(self, interaction: discord.Interaction, channel: str, message: str) -> None:
		# Send a message to a specific channel as the bot
		target_guild = discord.utils.get(self.bot.guilds, id=config.runserver)
		if target_guild is None:
			await send_ephemeral(interaction, embed=error_embed('**Error**: Could not resolve target server.'))
			return

		target_channel = discord.utils.get(target_guild.text_channels, name=channel)
		if target_channel is None:
			await send_ephemeral(
				interaction,
				embed=error_embed('**Error**: Can only send messages to existing text channels.'),
			)
			return

		sent_message = await target_channel.send(message)
		display_message = message if len(message) <= 1000 else f'{message[:997]}...'

		await send_ephemeral(
			interaction,
			embed=info_embed(
				f'**Channel**: {target_channel.mention}\n'
				f'**Link**: {sent_message.jump_url}\n'
				f'**Message**: {display_message}',
				colour=0x00FF00,
			),
		)
