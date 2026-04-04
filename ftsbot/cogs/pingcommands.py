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

	@app_commands.command(description='Ping a specific role with custom text (Reviewers only)')
	@app_commands.describe(
		role='Which role do you want to ping?',
		message='What message do you want to send?'
	)
	@app_commands.guild_only()
	@app_commands.autocomplete(role=autocomplete.pingable_roles)
	@app_commands.checks.has_any_role('Reviewer', 'Administrator') # You can add more roles here if needed
	async def ping(self, interaction: discord.Interaction, role: str, message: str):

		# Validate role exists in pingable_roles
		if role not in data.pingable_roles:
			available_roles = ', '.join(data.pingable_roles.values())
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xFF0000),
					description=f'**Error**: Invalid role. Available roles: {available_roles}'
				),
				ephemeral=True
			)
			return

		# Get the actual Discord role
		role_name = data.pingable_roles[role]
		discord_role = discord.utils.get(interaction.guild.roles, name=role_name)

		if discord_role is None:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xFF0000),
					description=f'**Error**: Role "{role_name}" not found in server'
				),
				ephemeral=True
			)
			return

		# Build the message with role mention
		ping_message = f"{discord_role.mention}\n{message}"
		
		# EXPLICITLY allow the bot to bypass the native ping restriction
		allowed_mentions = discord.AllowedMentions(roles=[discord_role])

		try:
			# Send the ping message to the channel
			await interaction.channel.send(content=ping_message, allowed_mentions=allowed_mentions)
			
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0x00FF00),
					description=f'**Success**: Pinged {discord_role.name} with your message'
				),
				ephemeral=True
			)
		except discord.Forbidden:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xFF0000),
					description='**Error**: Bot does not have permission to send messages or mention roles in this channel'
				),
				ephemeral=True
			)
		except Exception as e:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xFF0000),
					description=f'**Error**: {str(e)}'
				),
				ephemeral=True
			)

	# This catches the error if a normal user tries to run the command
	@ping.error
	async def on_ping_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
		if isinstance(error, app_commands.MissingAnyRole) or isinstance(error, app_commands.MissingRole):
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xFF0000),
					description='**Error**: Only Reviewers can use this command'
				),
				ephemeral=True
			)
		else:
			await interaction.response.send_message(str(error), ephemeral=True)

async def setup(bot):
	await bot.add_cog(pingcommands(bot))
