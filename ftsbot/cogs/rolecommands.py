#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from ftsbot import data
from ftsbot.functions import autocomplete
from ftsbot.utils.embeds import error_embed, info_embed, success_embed
from ftsbot.utils.interactions import defer_response, send_ephemeral

if TYPE_CHECKING:
	from ftsbot.liquipediabot import LiquipediaBot


class RoleCommands(commands.Cog):
	def __init__(self, bot: LiquipediaBot):
		self.bot = bot

	@app_commands.command(description='Get your Discord ID')
	async def discordid(self, interaction: discord.Interaction) -> None:
		await send_ephemeral(
			interaction,
			embed=info_embed(f'User "{interaction.user.name}" has ID "{interaction.user.id}"'),
		)

	@app_commands.command(description='Get your wiki roles')
	@app_commands.guild_only()
	async def wikiroles(self, interaction: discord.Interaction) -> None:
		if interaction.guild is None or not isinstance(interaction.user, discord.Member):
			await send_ephemeral(
				interaction, embed=error_embed('**Error**: This command can only be used in a server.')
			)
			return

		await defer_response(interaction, ephemeral=True)

		# Fetch the user's groups from the API
		result = await self.bot.tlintegration.get_wiki_roles(interaction.user.id)
		if result is None:
			await send_ephemeral(
				interaction,
				embed=error_embed(
					'**Error**: Could not fetch wiki roles. Please try again later or contact an admin if the problem persists.'
				),
			)
			return

		added_roles: list[str] = []

		# Sync Editor/Reviewer roles
		for role_id in result.groups:
			role_name = data.wikiroles.get(role_id)
			if role_name is None:
				continue

			role = discord.utils.get(interaction.guild.roles, name=role_name)
			if role is None or role in interaction.user.roles:
				continue

			try:
				await interaction.user.add_roles(role, reason='Wiki role sync')
			except discord.Forbidden:
				continue
			else:
				added_roles.append(role.name)

		# Grant the Silver Plus role if they got the coin
		if result.silver_plus:
			role = discord.utils.get(interaction.guild.roles, name='Silver Plus')
			if role is not None and role not in interaction.user.roles:
				try:
					await interaction.user.add_roles(role, reason='Wiki role sync')
				except discord.Forbidden:
					pass
				else:
					added_roles.append(role.name)

		if not added_roles:
			await send_ephemeral(
				interaction,
				embed=info_embed('No eligible wiki roles were found to add.'),
			)
			return

		role_list = ', '.join(added_roles)
		await send_ephemeral(
			interaction,
			embed=success_embed(f'**Success**: Added wiki role(s): {role_list}'),
		)

	@app_commands.command(description='Add a role to yourself')
	@app_commands.describe(role='Which role do you want to add?')
	@app_commands.guild_only()
	@app_commands.autocomplete(role=autocomplete.roles)
	async def addrole(self, interaction: discord.Interaction, role: str) -> None:
		if interaction.guild is None or not isinstance(interaction.user, discord.Member):
			await send_ephemeral(
				interaction, embed=error_embed('**Error**: This command can only be used in a server.')
			)
			return

		# Only allow assigning roles that are in the approved botroles list
		if role not in data.botroles:
			await send_ephemeral(
				interaction,
				embed=error_embed(f'**Error**: Can\'t add that role to "{interaction.user.name}"'),
			)
			return

		role_object = discord.utils.get(interaction.guild.roles, name=role)
		if role_object is None:
			await send_ephemeral(interaction, embed=error_embed('**Error**: Role not found on this server.'))
			return

		if role_object in interaction.user.roles:
			await send_ephemeral(
				interaction,
				embed=info_embed(f'You already have the role "{role_object.name}".'),
			)
			return

		try:
			await interaction.user.add_roles(role_object, reason='Self-assign role')
		except discord.Forbidden:
			await send_ephemeral(interaction, embed=error_embed('**Error**: Missing permissions to assign this role.'))
			return

		await send_ephemeral(
			interaction,
			embed=success_embed(f'**Success**: Role "{role_object.name}" added to "{interaction.user.name}"'),
		)

	@app_commands.command(description='Remove a role from yourself')
	@app_commands.describe(role='Which role do you want to remove?')
	@app_commands.guild_only()
	@app_commands.autocomplete(role=autocomplete.roles)
	async def removerole(self, interaction: discord.Interaction, role: str) -> None:
		if interaction.guild is None or not isinstance(interaction.user, discord.Member):
			await send_ephemeral(
				interaction, embed=error_embed('**Error**: This command can only be used in a server.')
			)
			return

		# Only allow removing roles that the bot is actually allowed to manage
		if role not in data.botroles:
			await send_ephemeral(
				interaction,
				embed=error_embed(f'**Error**: Can\'t remove that role from "{interaction.user.name}"'),
			)
			return

		role_object = discord.utils.get(interaction.guild.roles, name=role)
		if role_object is None:
			await send_ephemeral(interaction, embed=error_embed('**Error**: Role not found on this server.'))
			return

		if role_object not in interaction.user.roles:
			await send_ephemeral(
				interaction,
				embed=info_embed(f'You do not have the role "{role_object.name}".'),
			)
			return

		try:
			await interaction.user.remove_roles(role_object, reason='Self-remove role')
		except discord.Forbidden:
			await send_ephemeral(interaction, embed=error_embed('**Error**: Missing permissions to remove this role.'))
			return

		await send_ephemeral(
			interaction,
			embed=success_embed(f'**Success**: Role "{role_object.name}" removed from "{interaction.user.name}"'),
		)
