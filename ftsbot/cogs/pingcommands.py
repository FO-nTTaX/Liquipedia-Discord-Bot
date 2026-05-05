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
@app_commands.checks.has_any_role('Reviewer', 'Administrator')
async def ping(self, interaction: discord.Interaction, role: str, message: str):

    # Defer the response so the interaction doesn't timeout if Discord is slow
    await interaction.response.defer(ephemeral=True)

    # Validate role exists in pingable_roles list
    if role not in data.pingable_roles:
        available_roles = ', '.join(data.pingable_roles)
        await interaction.followup.send(
            embed=discord.Embed(
                colour=discord.Colour(0xFF0000),
                description=f'**Error**: Invalid role. Available roles: {available_roles}'
            )
        )
        return

    # Get the actual Discord role
    discord_role = discord.utils.get(interaction.guild.roles, name=role)

    if discord_role is None:
        await interaction.followup.send(
            embed=discord.Embed(
                colour=discord.Colour(0xFF0000),
                description=f'**Error**: Role "{role}" not found in server'
            )
        )
        return

    # Build the message with role mention AND attribution
    ping_message = f"{discord_role.mention}\n**Message from {interaction.user.mention}:**\n{message}"
    
    # Prevent crashing from Discord's 2k character limit
    if len(ping_message) > 2000:
        await interaction.followup.send(
            embed=discord.Embed(
                colour=discord.Colour(0xFF0000),
                description='**Error**: Your message is too long! It must be under 2000 characters.'
            )
        )
        return
    
    # EXPLICITLY allow the bot to bypass the native ping restriction
    allowed_mentions = discord.AllowedMentions(roles=[discord_role])

    try:
        # Send the ping message to the channel
        await interaction.channel.send(content=ping_message, allowed_mentions=allowed_mentions)
        
        await interaction.followup.send(
            embed=discord.Embed(
                colour=discord.Colour(0x00FF00),
                description=f'**Success**: Pinged {discord_role.name} with your message'
            )
        )
    except discord.Forbidden:
        await interaction.followup.send(
            embed=discord.Embed(
                colour=discord.Colour(0xFF0000),
                description='**Error**: Bot does not have permission to send messages or mention roles in this channel'
            )
        )
    except Exception as e:
        await interaction.followup.send(
            embed=discord.Embed(
                colour=discord.Colour(0xFF0000),
                description=f'**Error**: {str(e)}'
            )
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
