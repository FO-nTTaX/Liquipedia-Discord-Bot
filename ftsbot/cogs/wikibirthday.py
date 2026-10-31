# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

from __future__ import annotations

import logging
from datetime import UTC, date, datetime, time
from typing import TYPE_CHECKING

import discord
from discord.ext import commands, tasks

from ftsbot import data

if TYPE_CHECKING:
	from ftsbot.liquipediabot import LiquipediaBot

logger = logging.getLogger(__name__)


class WikiBirthday(commands.Cog):
	"""Posts a birthday message for wikis created on this day, once per day."""

	def __init__(self, bot: LiquipediaBot) -> None:
		self.bot = bot
		self._last_check_date: date | None = None

	async def cog_load(self) -> None:
		self.birthday_check.start()

	def cog_unload(self) -> None:
		self.birthday_check.cancel()

	@staticmethod
	def _birthdays_on(day: date) -> list[tuple[str, str, date]]:
		"""Return (wiki, display_name, creation_date) for all wikis with a birthday on *day*."""
		birthdays: list[tuple[str, str, date]] = []
		for wiki, (created, name, _colour) in data.wiki_birthdays.items():
			created_date = date(*map(int, created.split('-')))
			if (created_date.month, created_date.day) == (day.month, day.day):
				birthdays.append((wiki, name, created_date))
		return birthdays

	def _build_embed(self, wiki: str, name: str, created: date, day: date) -> discord.Embed:
		url = f'{data.wikibaseurl}{wiki}'
		age = day.year - created.year
		years = 'year' if age == 1 else 'years'
		desc = f'**[{name}]({url})** wiki turns **{age} {years}** old today!'

		entry = data.wiki_birthdays.get(wiki)
		colour = 0xFF2400 if entry is None else int(entry[2], 16)

		return discord.Embed(
			title='🎂 Happy Birthday!',
			description=desc,
			colour=discord.Colour(colour),
		).set_footer(text=f'Wiki created on {created:%d %B %Y}')

	async def _send_birthday_announcement(self, birthdays: list[tuple[str, str, date]], day: date) -> None:
		for wiki, name, created in birthdays:
			channel = self._channel_for_wiki(wiki)
			if channel is None:
				logger.warning('No channel named #%s found for wiki birthday, skipping %s', wiki, name)
				continue

			embed = self._build_embed(wiki, name, created, day)
			try:
				await channel.send(embed=embed)
			except discord.Forbidden:
				logger.warning('Missing permissions to send birthday message to #%s', channel.name)

	def _channel_for_wiki(self, wiki: str) -> discord.TextChannel | None:
		"""Return the first text channel whose name matches the wiki slug."""
		for guild in self.bot.guilds:
			for channel in guild.text_channels:
				if channel.name == wiki:
					return channel
		return None

	@tasks.loop(time=time(hour=0, minute=0, tzinfo=UTC))
	async def birthday_check(self) -> None:
		today = datetime.now(UTC).date()
		if today == self._last_check_date:
			return
		self._last_check_date = today

		birthdays = self._birthdays_on(today)
		if not birthdays:
			return

		await self._send_birthday_announcement(birthdays, today)

	@birthday_check.before_loop
	async def before_birthday_check(self) -> None:
		await self.bot.wait_until_ready()
