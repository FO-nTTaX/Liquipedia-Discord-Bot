#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 4.1.1

from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from ftsbot import data
from ftsbot.functions import autocomplete
from ftsbot.utils.embeds import error_embed, success_embed
from ftsbot.utils.interactions import defer_response, send_ephemeral

if TYPE_CHECKING:
	from ftsbot.liquipediabot import LiquipediaBot


class PingCommands(commands.Cog):
	def __init__(self, bot: LiquipediaBot):
		self.bot = bot
		self._pingable_roles_casefold = {role.casefold(): role for role in data.pingable_roles}

	@app_commands.command(description='Ping a specific role (Reviewer+)')
	@app_commands.describe(role='Which role do you want to ping?')
	@app_commands.guild_only()
	@app_commands.autocomplete(role=autocomplete.pingable_roles)
	@app_commands.checks.has_any_role(*data.ping_command_roles)
	async def ping(self, interaction: discord.Interaction, role: str) -> None:
		await defer_response(interaction, ephemeral=True)

		role_name = self._pingable_roles_casefold.get(role.casefold())
		if role_name is None:
			await send_ephemeral(
				interaction,
				embed=error_embed(f'**Error**: Role "{role}" is not an approved pingable role.'),
			)
			return

		if interaction.guild is None:
			await send_ephemeral(
				interaction, embed=error_embed('**Error**: This command can only be used in a server.')
			)
			return

		if interaction.channel is None:
			await send_ephemeral(interaction, embed=error_embed('**Error**: Could not resolve channel.'))
			return

		discord_role = discord.utils.get(interaction.guild.roles, name=role_name)
		if discord_role is None:
			await send_ephemeral(
				interaction,
				embed=error_embed(
					f'**Error**: Role "{role_name}" no longer exists — please contact an admin to update the role list'
				),
			)
			return

		await interaction.channel.send(
			content=f'{discord_role.mention} *(Ping requested by {interaction.user.mention})*',
			allowed_mentions=discord.AllowedMentions(
				everyone=False,
				users=[interaction.user],
				roles=[discord_role],
			),
		)

		await send_ephemeral(interaction, embed=success_embed(f'Pinged {discord_role.name}!'))

	@ping.error
	async def on_ping_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		if isinstance(error, app_commands.MissingAnyRole):
			await send_ephemeral(
				interaction,
				embed=error_embed('**Error**: Only Reviewer+ can use this command.'),
			)
			return

		await send_ephemeral(
			interaction,
			embed=error_embed('**Error**: Could not execute ping command.'),
		)
