#!/usr/bin/env python3

# License MIT
# Copyright 2016-2025 Alex Winkler
# Version 4.1.0

import discord
from discord import app_commands
from discord.ext import commands
from ftsbot import config, data
from ftsbot.functions import autocomplete


class pingcommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_reviewer(self, interaction: discord.Interaction) -> bool:
        """Check if user has reviewer role"""
        user_roles = [role.name for role in interaction.user.roles]
        return data.reviewer_role in user_roles

    @app_commands.command(description='Ping a specific role with custom text (Reviewers only)')
    @app_commands.describe(
        role='Which role do you want to ping?',
        message='What message do you want to send?'
    )
    @app_commands.guild_only()
    @app_commands.autocomplete(role=autocomplete.pingable_roles)
    async def ping(
        self,
        interaction: discord.Interaction,
        role: str,
        message: str
    ):
        """
        Command to ping specific roles with custom text.
        Only accessible to reviewers.
        """
        # Check permissions
        if not self.is_reviewer(interaction):
            await interaction.response.send_message(
                embed=discord.Embed(
                    colour=discord.Colour(0xFF0000),
                    description='**Error**: Only reviewers can use this command'
                ),
                ephemeral=True
            )
            return

        # Validate role exists in pingable_roles
        if role not in data.pingable_roles:
            available_roles = ', '.join(data.pingable_roles.keys())
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

        try:
            # Send the ping message to the channel
            await interaction.channel.send(ping_message)
            
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
                    description='**Error**: Bot does not have permission to mention this role'
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


async def setup(bot):
    await bot.add_cog(pingcommands(bot))
