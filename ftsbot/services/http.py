#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 4.1.1

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any

import aiohttp


class HttpClientError(RuntimeError):
	pass


@dataclass(frozen=True)
class HttpResponseError(HttpClientError):
	status: int
	body: str

	def __str__(self) -> str:
		return f'HTTP {self.status}: {self.body[:500]}'


class HttpClient:
	def __init__(self) -> None:
		self._session: aiohttp.ClientSession | None = None
		self._timeout = aiohttp.ClientTimeout(total=15)

	async def start(self) -> None:
		if self._session is not None and not self._session.closed:
			return

		self._session = aiohttp.ClientSession(
			timeout=self._timeout,
			headers={
				'User-Agent': 'Liquipedia-Discord-Bot',
			},
		)

	async def close(self) -> None:
		if self._session is None:
			return
		await self._session.close()

	@property
	def session(self) -> aiohttp.ClientSession:
		if self._session is None or self._session.closed:
			raise HttpClientError('HTTP session is not started.')
		return self._session

	async def request_json(
		self,
		method: str,
		url: str,
		*,
		params: dict[str, Any] | None = None,
		data: dict[str, Any] | None = None,
	) -> dict[str, Any]:
		try:
			async with self.session.request(method, url, params=params, data=data) as response:
				body = await response.text()

				if response.status < 200 or response.status >= 300:
					raise HttpResponseError(status=response.status, body=body)

				try:
					parsed = json.loads(body)
				except json.JSONDecodeError as e:
					raise HttpClientError(f'Invalid JSON received from {url}') from e

				if not isinstance(parsed, dict):
					raise HttpClientError(f'Unexpected JSON payload received from {url}')

				return parsed
		except asyncio.TimeoutError as e:
			raise HttpClientError(f'Timed out while requesting {url}') from e
		except aiohttp.ClientError as e:
			raise HttpClientError(f'HTTP request failed for {url}') from e
