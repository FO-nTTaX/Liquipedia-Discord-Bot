#!/usr/bin/env python3

# License MIT
# Copyright 2016-2022 Alex Winkler
# Version 4.0.0

from discord import app_commands
from ftsbot import data

def wiki(current: str):
	wikis = [
		wiki
		for wiki in data.wikis if current.lower() in wiki.lower()
	]

	def sortwikis(element):
		return element.index(current)
	wikis.sort(key=sortwikis)

	return [
		app_commands.Choice(name=wiki, value=wiki)
		for wiki in wikis
	][:25]

