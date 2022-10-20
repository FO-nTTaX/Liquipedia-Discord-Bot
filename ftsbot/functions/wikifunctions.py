#!/usr/bin/env python3

# License MIT
# Copyright 2016-2022 Alex Winkler
# Version 4.0.2

import random
import requests
import json
import urllib
from ftsbot import data


def pendingchanges(
	wiki
):
	result = ''
	url = (
		data.wikibaseurl
		+ wiki
		+ '/api.php?action=query&format=json&list=oldreviewedpages&ornamespace=0|10&orlimit=500'
	)
	jsonobj = requests.post(url).json()
	results = jsonobj['query']['oldreviewedpages']
	count = len(results)
	if count == 0:
		result = 'No pending changes on ' + wiki
	elif count > 0:
		random.shuffle(results)
		plural = 's'
		if count == 1:
			plural = ''
		if count == 500:
			countstr = 'over 500'
		else:
			countstr = str(count)
		result = (
			'**[Pages with pending changes]('
			+ data.wikibaseurl
			+ wiki
			+ '/Special:PendingChanges)**: ('
			+ countstr
			+ ' page'
			+ plural
			+ ' pending)'
		)
		for i in range(0, min(count, 5)):
			result += (
				'\n- ['
				+ results[i]['title']
				+ ']('
				+ data.wikibaseurl
				+ wiki
				+ '/'
				+ urllib.parse.quote(results[i]['title'].replace(' ', '_'))
				+ ') (diff: '
				+ str(results[i]['diff_size'])
				+ ', since: '
				+ results[i]['pending_since'][0:10]
				+ ')'
			)
	return result


def unreviewedpages(
	wiki
):
	result = ''
	url = (
		data.wikibaseurl
		+ wiki
		+ '/api.php?action=query&format=json&list=unreviewedpages&urfilterredir=nonredirects'
		+ '&urnamespace=0|10&urlimit=500'
	)
	jsonobj = requests.post(url).json()
	results = jsonobj['query']['unreviewedpages']
	count = len(results)
	if count == 0:
		result = 'No unreviewed pages on ' + wiki
	elif count > 0:
		random.shuffle(results)
		plural = 's'
		if count == 1:
			plural = ''
		if count == 500:
			countstr = 'over 500'
		else:
			countstr = str(count)
		result = (
			'**[Unreviewed pages]('
			+ data.wikibaseurl
			+ wiki
			+ '/Special:UnreviewedPages)**: ('
			+ countstr
			+ ' page'
			+ plural
			+ ' unreviewed)'
		)
		for i in range(0, min(count, 5)):
			result += (
				'\n- ['
				+ results[i]['title']
				+ ']('
				+ data.wikibaseurl
				+ wiki
				+ '/'
				+ urllib.parse.quote(results[i]['title'].replace(' ', '_'))
				+ ')'
			)
	return result


def search(
	wiki,
	searchstring
):
	result = ''
	url = data.wikibaseurl + wiki + '/api.php?action=query&format=json&list=search&srlimit=5&srsearch=' + searchstring
	jsonobj = requests.post(url).json()
	results = jsonobj['query']['search']
	count = jsonobj['query']['searchinfo']['totalhits']
	if count == 0:
		result = 'No results for **' + searchstring + '** on ' + wiki
	elif count > 0:
		plural = 's'
		if count == 1:
			plural = ''
		else:
			countstr = str(count)
		result = (
			'**[Search results]('
			+ data.wikibaseurl
			+ wiki
			+ '/index.php?title=Special%3ASearch&profile=default&search='
			+ searchstring.replace(' ', '+')
			+ '&fulltext=Search)**: ('
			+ countstr
			+ ' page'
			+ plural
			+ ')'
		)
		for i in range(0, min(count, 5)):
			result += (
				'\n- ['
				+ results[i]['title']
				+ ']('
				+ data.wikibaseurl
				+ wiki
				+ '/'
				+ urllib.parse.quote(results[i]['title'].replace(' ', '_'))
				+ ')'
			)
	return result
