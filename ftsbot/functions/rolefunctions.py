# -*- coding: utf-8 -*-

# License MIT
# Copyright 2016-2021 Alex Winkler
# Version 3.0.0

import random
import requests
import json
import urllib
from ftsbot import data, secrets

def wikiroles(discordid):
	url = data.wikibaseurl + 'commons/api.php?format=json&action=teamliquidintegration-discordids'
	payload = {
		'discordid': discordid,
		'apikey': secrets.apikey
	}
	jsonobj = requests.post(url, data=payload).json()
	if 'error' in jsonobj:
		return False
	else:
		return [jsonobj['teamliquidintegration-discordids']['groups'],jsonobj['teamliquidintegration-discordids']['silverplus']]