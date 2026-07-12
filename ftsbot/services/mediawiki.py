#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

from __future__ import annotations

import urllib.parse
from dataclasses import dataclass
from typing import Any

from cachetools import TTLCache

from ftsbot import data
from ftsbot.services.http import HttpClient


@dataclass(frozen=True)
class PendingChange:
	title: str
	diff_size: int
	pending_since: str


@dataclass(frozen=True)
class PageItem:
	title: str


@dataclass(frozen=True)
class SearchResults:
	total_hits: int
	items: tuple[PageItem, ...]


class MediaWikiService:
	def __init__(self, http_client: HttpClient) -> None:
		self._http_client = http_client
		self._pending_cache: TTLCache[str, tuple[PendingChange, ...]] = TTLCache(maxsize=256, ttl=60)
		self._unreviewed_cache: TTLCache[str, tuple[PageItem, ...]] = TTLCache(maxsize=256, ttl=60)
		self._search_cache: TTLCache[tuple[str, str], SearchResults] = TTLCache(maxsize=512, ttl=300)

	def _api_url(self, wiki: str) -> str:
		return f'{data.wikibaseurl}{wiki}/api.php'

	def page_url(self, wiki: str, title: str) -> str:
		return f'{data.wikibaseurl}{wiki}/{urllib.parse.quote(title.replace(" ", "_"))}'

	def pending_changes_url(self, wiki: str) -> str:
		return f'{data.wikibaseurl}{wiki}/Special:PendingChanges'

	def unreviewed_pages_url(self, wiki: str) -> str:
		return f'{data.wikibaseurl}{wiki}/Special:UnreviewedPages'

	def search_url(self, wiki: str, query: str) -> str:
		encoded_query = urllib.parse.quote_plus(query)
		return (
			f'{data.wikibaseurl}{wiki}/index.php?title=Special%3ASearch&profile=default'
			f'&search={encoded_query}&fulltext=Search'
		)

	async def _query(self, wiki: str, *, params: dict[str, Any]) -> dict[str, Any]:
		base_params = {
			'action': 'query',
			'format': 'json',
		}
		base_params.update(params)
		return await self._http_client.request_json('GET', self._api_url(wiki), params=base_params)

	async def get_pending_changes(self, wiki: str) -> tuple[PendingChange, ...]:
		if wiki in self._pending_cache:
			return self._pending_cache[wiki]

		jsonobj = await self._query(
			wiki,
			params={
				'list': 'oldreviewedpages',
				'ornamespace': '0|10',
				'orlimit': '500',
			},
		)

		results = ((jsonobj.get('query') or {}).get('oldreviewedpages')) or []
		items: list[PendingChange] = []

		for result in results:
			if not isinstance(result, dict):
				continue

			title = result.get('title')
			if not isinstance(title, str):
				continue

			try:
				diff_size = int(result.get('diff_size') or 0)
			except (TypeError, ValueError):
				diff_size = 0

			pending_since = result.get('pending_since')
			if not isinstance(pending_since, str):
				pending_since = ''

			items.append(
				PendingChange(
					title=title,
					diff_size=diff_size,
					pending_since=pending_since,
				)
			)

		value = tuple(items)
		self._pending_cache[wiki] = value
		return value

	async def get_unreviewed_pages(self, wiki: str) -> tuple[PageItem, ...]:
		if wiki in self._unreviewed_cache:
			return self._unreviewed_cache[wiki]

		jsonobj = await self._query(
			wiki,
			params={
				'list': 'unreviewedpages',
				'urfilterredir': 'nonredirects',
				'urnamespace': '0|10',
				'urlimit': '500',
			},
		)

		results = ((jsonobj.get('query') or {}).get('unreviewedpages')) or []
		items: list[PageItem] = []

		for result in results:
			if not isinstance(result, dict):
				continue

			title = result.get('title')
			if not isinstance(title, str):
				continue

			items.append(PageItem(title=title))

		value = tuple(items)
		self._unreviewed_cache[wiki] = value
		return value

	async def search_pages(self, wiki: str, query: str) -> SearchResults:
		cache_key = (wiki, query.casefold())
		if cache_key in self._search_cache:
			return self._search_cache[cache_key]

		jsonobj = await self._query(
			wiki,
			params={
				'list': 'search',
				'srlimit': '5',
				'srsearch': query,
			},
		)

		searchinfo = (jsonobj.get('query') or {}).get('searchinfo') or {}
		try:
			total_hits = int(searchinfo.get('totalhits') or 0)
		except (TypeError, ValueError):
			total_hits = 0

		results = ((jsonobj.get('query') or {}).get('search')) or []
		items: list[PageItem] = []

		for result in results:
			if not isinstance(result, dict):
				continue

			title = result.get('title')
			if not isinstance(title, str):
				continue

			items.append(PageItem(title=title))

		value = SearchResults(total_hits=total_hits, items=tuple(items))
		self._search_cache[cache_key] = value
		return value
