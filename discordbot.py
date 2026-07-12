#!/usr/bin/env python3

# License MIT
# Copyright 2016-2026 Alex Winkler
# Version 5.0.0

import os

from dotenv import load_dotenv

from ftsbot.liquipediabot import LiquipediaBot


def _require_env(name: str) -> str:
	value = os.environ.get(name)
	if value is None or not value.strip():
		raise RuntimeError(f'Missing required environment variable: {name}')
	return value.strip()


def main() -> None:
	load_dotenv()

	token = _require_env('token')
	apikey = os.environ.get('apikey')
	apikey = apikey.strip() if apikey and apikey.strip() else None

	bot = LiquipediaBot(apikey=apikey)
	bot.run(token)


if __name__ == '__main__':
	main()
