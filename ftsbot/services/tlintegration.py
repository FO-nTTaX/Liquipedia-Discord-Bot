#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

from __future__ import annotations

from dataclasses import dataclass

from cachetools import TTLCache

from ftsbot import data
from ftsbot.services.http import HttpClient, HttpClientError


@dataclass(frozen=True)
class WikiRolesResult:
	groups: tuple[str, ...]
	silver_plus: bool


class TLIntegrationService:
	def __init__(self, http_client: HttpClient, *, apikey: str | None) -> None:
		self._http_client = http_client
		self._apikey = apikey
		self._cache: TTLCache[int, WikiRolesResult] = TTLCache(maxsize=1024, ttl=600)

	def _api_url(self) -> str:
		return f'{data.wikibaseurl}commons/api.php'

	async def get_wiki_roles(self, discord_id: int) -> WikiRolesResult | None:
		if discord_id in self._cache:
			return self._cache[discord_id]

		if not self._apikey:
			return None

		try:
			jsonobj = await self._http_client.request_json(
				'POST',
				self._api_url(),
				params={
					'format': 'json',
					'action': 'teamliquidintegration-discordids',
				},
				data={
					'discordid': str(discord_id),
					'apikey': self._apikey,
				},
			)
		except HttpClientError:
			return None

		if 'error' in jsonobj:
			return None

		payload = jsonobj.get('teamliquidintegration-discordids')
		if not isinstance(payload, dict):
			return None

		raw_groups = payload.get('groups')
		if not isinstance(raw_groups, list):
			return None

		try:
			silver_plus = bool(int(payload.get('silverplus') or 0))
		except (TypeError, ValueError):
			silver_plus = False

		result = WikiRolesResult(
			groups=tuple(str(group) for group in raw_groups),
			silver_plus=silver_plus,
		)
		self._cache[discord_id] = result
		return result
