#!/usr/bin/env python3

# License MIT
# Copyright 2016-2025 Alex Winkler
# Version 4.1.0

import discord
from discord import app_commands
from discord.ext import commands

from ftsbot import data
from ftsbot.functions import autocomplete


class pingcommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._pingable_roles_casefold = {r.casefold(): r for r in data.pingable_roles}

	async def _reply_ephemeral(self, interaction: discord.Interaction, *, embed: discord.Embed):
		if interaction.response.is_done():
			await interaction.followup.send(embed=embed, ephemeral=True)
		else:
			await interaction.response.send_message(embed=embed, ephemeral=True)

	@app_commands.command(description='Ping a specific role (Reviewer+)')
	@app_commands.describe(role='Which role do you want to ping?')
	@app_commands.guild_only()
	@app_commands.autocomplete(role=autocomplete.pingable_roles)
	@app_commands.checks.has_any_role('Reviewer', 'Administrator', 'Discord Admins', 'Liquipedia Employee')
	async def ping(self, interaction: discord.Interaction, role: str):
		await interaction.response.defer(ephemeral=True)

		role_name = self._pingable_roles_casefold.get(role.casefold())
		if role_name is None:
			await interaction.followup.send(
				embed=discord.Embed(
					colour=discord.Colour(0xFF0000),
					description=f'**Error**: Role "{role}" is not an approved pingable role.',
				)
			)
			return

		discord_role = discord.utils.get(interaction.guild.roles, name=role_name)
		if discord_role is None:
			await interaction.followup.send(
				embed=discord.Embed(
					colour=discord.Colour(0xFF0000),
					description=(
						f'**Error**: Role "{role_name}" no longer exists — please contact an admin to update the role list'
					),
				)
			)
			return

		await interaction.channel.send(
			content=f'{discord_role.mention} *(Ping requested by {interaction.user.mention})*',
			allowed_mentions=discord.AllowedMentions(everyone=False, users=[interaction.user], roles=[discord_role]),
		)

		await interaction.followup.send(
			embed=discord.Embed(
				colour=discord.Colour(0x00FF00),
				description=f'Pinged {discord_role.name}!',
			)
		)

	@ping.error
	async def on_ping_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
		if isinstance(error, app_commands.MissingAnyRole):
			await self._reply_ephemeral(
				interaction,
				embed=discord.Embed(
					colour=discord.Colour(0xFF0000),
					description='**Error**: Only Reviewer+ can use this command.',
				),
			)
			return

		await self._reply_ephemeral(
			interaction,
			embed=discord.Embed(
				colour=discord.Colour(0xFF0000),
				description='**Error**: Could not execute ping command.',
			),
		)
