#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

from __future__ import annotations

import random
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from ftsbot import data
from ftsbot.functions import autocomplete
from ftsbot.services.http import HttpClientError
from ftsbot.services.mediawiki import PageItem, PendingChange
from ftsbot.utils.embeds import error_embed, success_embed
from ftsbot.utils.interactions import defer_response, send_message

if TYPE_CHECKING:
	from ftsbot.liquipediabot import LiquipediaBot


class WikiCommands(commands.Cog):
	def __init__(self, bot: LiquipediaBot):
		self.bot = bot

	def _resolve_wiki(self, interaction: discord.Interaction, wiki: str | None) -> str | None:
		if wiki in data.wikis:
			return wiki

		if isinstance(interaction.channel, discord.TextChannel) and interaction.channel.name in data.wikis:
			return interaction.channel.name

		return None

	def _format_pending_changes(
		self,
		wiki: str,
		count: int,
		items: tuple[PendingChange, ...],
	) -> str:
		if count == 0:
			return f'No pending changes on {wiki}'

		plural = '' if count == 1 else 's'
		countstr = 'over 500' if count == 500 else str(count)

		result = (
			f'**[Pages with pending changes]({self.bot.mediawiki.pending_changes_url(wiki)})**: '
			f'({countstr} page{plural} pending)'
		)

		for item in random.sample(items, k=min(count, 5)):
			since = item.pending_since[:10] if item.pending_since else ''
			result += (
				f'\n- [{item.title}]({self.bot.mediawiki.page_url(wiki, item.title)}) '
				f'(diff: {item.diff_size}, since: {since})'
			)

		return result

	def _format_unreviewed_pages(
		self,
		wiki: str,
		count: int,
		items: tuple[PageItem, ...],
	) -> str:
		if count == 0:
			return f'No unreviewed pages on {wiki}'

		plural = '' if count == 1 else 's'
		countstr = 'over 500' if count == 500 else str(count)

		result = (
			f'**[Unreviewed pages]({self.bot.mediawiki.unreviewed_pages_url(wiki)})**: '
			f'({countstr} page{plural} unreviewed)'
		)

		for item in random.sample(items, k=min(count, 5)):
			result += f'\n- [{item.title}]({self.bot.mediawiki.page_url(wiki, item.title)})'

		return result

	def _format_search_results(
		self,
		wiki: str,
		query: str,
		total_hits: int,
		items: tuple[PageItem, ...],
	) -> str:
		if total_hits == 0:
			return f'No results for **{query}** on {wiki}'

		plural = '' if total_hits == 1 else 's'
		countstr = str(total_hits)

		result = f'**[Search results]({self.bot.mediawiki.search_url(wiki, query)})**: ({countstr} page{plural})'
		for item in items[:5]:
			result += f'\n- [{item.title}]({self.bot.mediawiki.page_url(wiki, item.title)})'

		return result

	@app_commands.command(description='See pending changes')
	@app_commands.describe(wiki='Which wiki do you want the pending changes of?')
	@app_commands.autocomplete(wiki=autocomplete.wiki)
	async def pendingchanges(self, interaction: discord.Interaction, wiki: str | None) -> None:
		usewiki = self._resolve_wiki(interaction, wiki)
		if usewiki is None:
			await send_message(interaction, embed=error_embed('There seems to be no wiki with such a url!'))
			return

		await defer_response(interaction)

		try:
			items = await self.bot.mediawiki.get_pending_changes(usewiki)
		except HttpClientError:
			await send_message(interaction, embed=error_embed('**Error**: Could not fetch pending changes.'))
			return

		result = self._format_pending_changes(usewiki, len(items), items)
		await send_message(interaction, embed=success_embed(result))

	@app_commands.command(description='See unreviewed pages')
	@app_commands.describe(wiki='Which wiki do you want the unreviewed pages of?')
	@app_commands.autocomplete(wiki=autocomplete.wiki)
	async def unreviewedpages(self, interaction: discord.Interaction, wiki: str | None) -> None:
		usewiki = self._resolve_wiki(interaction, wiki)
		if usewiki is None:
			await send_message(interaction, embed=error_embed('There seems to be no wiki with such a url!'))
			return

		await defer_response(interaction)

		try:
			items = await self.bot.mediawiki.get_unreviewed_pages(usewiki)
		except HttpClientError:
			await send_message(interaction, embed=error_embed('**Error**: Could not fetch unreviewed pages.'))
			return

		result = self._format_unreviewed_pages(usewiki, len(items), items)
		await send_message(interaction, embed=success_embed(result))

	@app_commands.command(description='Search Liquipedia')
	@app_commands.describe(search='What do you want to search?', wiki='Which wiki do you want to search?')
	@app_commands.autocomplete(wiki=autocomplete.wiki)
	async def search(self, interaction: discord.Interaction, search: str, wiki: str | None) -> None:
		usewiki = self._resolve_wiki(interaction, wiki)
		if usewiki is None:
			await send_message(interaction, embed=error_embed('There seems to be no wiki with such a url!'))
			return

		await defer_response(interaction)

		try:
			result = await self.bot.mediawiki.search_pages(usewiki, search)
		except HttpClientError:
			await send_message(interaction, embed=error_embed('**Error**: Could not search Liquipedia.'))
			return

		description = self._format_search_results(usewiki, search, result.total_hits, result.items)
		await send_message(interaction, embed=success_embed(description))
