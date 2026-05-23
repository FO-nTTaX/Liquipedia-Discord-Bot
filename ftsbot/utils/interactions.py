#!/usr/bin/env python3

from __future__ import annotations

import discord


async def defer_response(interaction: discord.Interaction, *, ephemeral: bool = False) -> None:
	if not interaction.response.is_done():
		await interaction.response.defer(ephemeral=ephemeral)


async def send_ephemeral(
	interaction: discord.Interaction,
	*,
	content: str | None = None,
	embed: discord.Embed | None = None,
) -> None:
	if interaction.response.is_done():
		await interaction.followup.send(content=content, embed=embed, ephemeral=True)
	else:
		await interaction.response.send_message(content=content, embed=embed, ephemeral=True)


async def send_message(
	interaction: discord.Interaction,
	*,
	content: str | None = None,
	embed: discord.Embed | None = None,
) -> None:
	if interaction.response.is_done():
		await interaction.followup.send(content=content, embed=embed)
	else:
		await interaction.response.send_message(content=content, embed=embed)
