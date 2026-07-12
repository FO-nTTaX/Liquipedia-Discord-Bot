#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 4.1.1

from __future__ import annotations

import discord


def error_embed(description: str) -> discord.Embed:
	return discord.Embed(colour=discord.Colour(0xFF0000), description=description)


def success_embed(description: str) -> discord.Embed:
	return discord.Embed(colour=discord.Colour(0x00FF00), description=description)


def info_embed(description: str, *, title: str | None = None, colour: int = 0x00FFFF) -> discord.Embed:
	embed = discord.Embed(colour=discord.Colour(colour), description=description)
	if title is not None:
		embed.title = title
	return embed


def accent_embed(description: str, *, title: str | None = None) -> discord.Embed:
	return info_embed(description, title=title, colour=0x663399)
