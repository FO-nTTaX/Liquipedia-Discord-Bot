#!/usr/bin/env python3

# License MIT
# Copyright 2016-2022 Alex Winkler
# Version 4.0.3

import requests
from ftsbot import data, secrets


def wikiroles(
	discordid
):
	url = data.wikibaseurl + 'commons/api.php?format=json&action=teamliquidintegration-discordids'
	payload = {
		'discordid': discordid,
		'apikey': secrets.apikey.strip()
	}
	jsonobj = requests.post(url, data=payload).json()
	if 'error' in jsonobj:
		return False
	else:
		return [
			jsonobj['teamliquidintegration-discordids']['groups'],
			jsonobj['teamliquidintegration-discordids']['silverplus']
		]
