#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

from __future__ import annotations

import discord
from discord import app_commands

from ftsbot import data


def _build_choices(values: list[str], current: str) -> list[app_commands.Choice[str]]:
	current_lower = current.casefold()

	matches = [value for value in values if current_lower in value.casefold()]
	matches.sort(key=lambda value: (value.casefold().index(current_lower), value.casefold()))

	return [app_commands.Choice(name=value, value=value) for value in matches[:25]]


async def wiki(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
	del interaction
	return _build_choices(data.wikis, current)


async def roles(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
	del interaction
	return _build_choices(data.botroles, current)


async def pingable_roles(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
	del interaction
	return _build_choices(data.pingable_roles, current)
