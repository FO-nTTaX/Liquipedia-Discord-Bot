#!/usr/bin/env python3

# License MIT
# Copyright 2016-2022 Alex Winkler
# Version 4.0.1

import discord
from discord import app_commands
from ftsbot import data

async def wiki(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
	wikis = [
		wiki
		for wiki in data.wikis if current.lower() in wiki.lower()
	]

	def sortwikis(element):
		return element.lower().index(current.lower())
	wikis.sort(key=sortwikis)

	return [
		app_commands.Choice(name=wiki, value=wiki)
		for wiki in wikis
	][:25]

async def roles(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
	roles = [
		role
		for role in data.botroles if current.lower() in role.lower()
	]

	def sortroles(element):
		return element.lower().index(current.lower())
	roles.sort(key=sortroles)

	return [
		app_commands.Choice(name=role, value=role)
		for role in roles
	][:25]
