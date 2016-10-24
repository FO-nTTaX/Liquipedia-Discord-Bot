# -*- coding: latin-1 -*-

import discord
import random
import requests
import json
import time

client = discord.Client()

muted = False
timestamp = round(time.time())

wikibaseurl = 'http://wiki.teamliquid.net/'
wikis = [
	'starcraft',
	'starcraft2',
	'dota2',
	'hearthstone',
	'heroes',
	'smash',
	'counterstrike',
	'overwatch',
	'commons',
	'warcraft',
	'fighters',
	'rocketleague',
	'clashroyale'
]
botroles = {
	'starcraft': 'Starcraft',
	'starcraft2': 'Starcraft 2',
	'dota2': 'Dota 2',
	'hearthstone': 'Hearthstone',
	'heroes': 'Heroes',
	'smash': 'Smash',
	'counterstrike': 'Counter-Strike',
	'overwatch': 'Overwatch',
	'commons': 'Commons',
	'warcraft': 'Warcraft',
	'fighters': 'Fighters',
	'rocketleague': 'Rocket League',
	'clashroyale': 'Clash Royale'
}
newchannelmessage = {}
for wiki in wikis:
	newchannelmessage[wiki] = False

def pendingchanges(wiki, displaynochanges):
	global wikibaseurl
	global wikis
	global newchannelmessage
	result = ''
	if wiki in wikis:
		if newchannelmessage[wiki] or displaynochanges:
			newchannelmessage[wiki] = False
			url = wikibaseurl + wiki + '/api.php?action=query&format=json&list=oldreviewedpages&ornamespace=0|10&orlimit=' + str(random.randrange(200, 500, 1))
			jsonobj = requests.get(url).json()
			results = jsonobj['query']['oldreviewedpages']
			count = len(results)
			if count == 0 and displaynochanges:
				result = 'No pending changes on ' + wiki
			elif count > 0:
				random.shuffle(results)
				plural = 's'
				if count == 1:
					plural = ''
				if count > 200:
					countstr = 'over 200'
				else:
					countstr = str(count)
				result = '**Pages with pending changes**: ' + wikibaseurl + wiki + '/Special:PendingChanges (' + countstr + ' page' + plural + ' pending)'
				for i in range(0, min(count, 5)):
					result += '\n' + wikibaseurl + wiki + '/' + results[i]['title'].replace(' ', '_') + ' (diff: ' + str(results[i]['diff_size']) + ', since: ' + results[i]['pending_since'][0:10] + ')'
	else:
		result = wikibaseurl + wiki + ' is not a wiki url we have!'
	return result

def unreviewedpages(wiki, displaynochanges):
	global wikibaseurl
	global wikis
	global newchannelmessage
	result = ''
	if wiki in wikis:
		if newchannelmessage[wiki] or displaynochanges:
			newchannelmessage[wiki] = False
			url = wikibaseurl + wiki + '/api.php?action=query&format=json&list=unreviewedpages&urfilterredir=nonredirects&urnamespace=0|10&urlimit=' + str(random.randrange(200, 500, 1))
			jsonobj = requests.get(url).json()
			results = jsonobj['query']['unreviewedpages']
			count = len(results)
			if count == 0 and displaynochanges:
				result = 'No unreviewed pages on ' + wiki
			elif count > 0:
				random.shuffle(results)
				plural = 's'
				if count == 1:
					plural = ''
				if count > 200:
					countstr = 'over 200'
				else:
					countstr = str(count)
				result = '**Unreviewed pages**: ' + wikibaseurl + wiki + '/Special:UnreviewedPages (' + countstr + ' page' + plural + ' pending)'
				for i in range(0, min(count, 5)):
					result += '\n' + wikibaseurl + wiki + '/' + results[i]['title'].replace(' ', '_')
	else:
		result = wikibaseurl + wiki + ' is not a wiki url we have!'
	return result

@client.async_event
def on_message(message):
	global muted
	global timestamp
	global newchannelmessage
	global botroles
	newchannelmessage[message.channel.name] = True
	if message.content == '!fobot' or message.content.startswith('!fobot'):
		if not muted:
			if message.content == '!fobot liquipedia':
				yield from client.send_message(message.channel, '**Liquipedia** is awesome! Use !fobot help to see the manual.')
			elif message.content == '!fobot guides':
				yield from client.send_message(message.channel, '**Liquipedia-Guides**: http://wiki.teamliquid.net/starcraft2/User:FO-BoT#Guides')
			elif message.content == '!fobot hype':
				yield from client.send_message(message.channel, '**\\\\Ü/ HYPE \\\\Ü/** http://stuff.gramma.name/hype/')
			elif message.content == '!fobot todo':
				yield from client.send_message(message.channel, '**Liquipedia-To Do Lists**: http://wiki.teamliquid.net/starcraft2/User:FO-BoT#To_Do_Lists')
			elif message.content == '!fobot dance':
				yield from client.send_message(message.channel, '**EVERYBODY DANCE \\\\Ü/**\n*dances :D\\\\-<*\n*dances :D|-<*\n*dances :D/-<*')
			elif message.content == '!fobot help':
				yield from client.send_message(message.channel, '**FO-BoT Commands**: http://wiki.teamliquid.net/starcraft2/User:FO-BoT#Manual')
			elif message.content == '!fobot lie':
				yield from client.send_message(message.channel, 'Liquipedia is not awesome... (good that this is a lie ^^)')
			elif message.content.startswith('!fobot talk ') and message.server == None and message.author.id == '138719439834185728':
				yield from client.send_message(message.channel, 'Hello ' + message.author.name)
			elif message.content == '!fobot coder':
				yield from client.send_message(message.channel, 'FO-BoT was coded by **FO-nTTaX**')
			elif message.content == '!fobot ranking':
				yield from client.send_message(message.channel, '**Liquipedia ranking**: http://www.tolueno.fr/liquipedia/editcount/')
			elif message.content == '!fobot pendingchanges':
				result = pendingchanges(message.channel.name, True)
				if result != '':
					yield from client.send_message(message.channel, result)
			elif message.content.startswith('!fobot pendingchanges '):
				result = pendingchanges(message.content.replace('!fobot pendingchanges ', ''), True)
				if result != '':
					yield from client.send_message(message.channel, result)
			elif message.content == '!fobot unreviewedpages':
				result = unreviewedpages(message.channel.name, True)
				if result != '':
					yield from client.send_message(message.channel, result)
			elif message.content.startswith('!fobot unreviewedpages '):
				result = unreviewedpages(message.content.replace('!fobot unreviewedpages ', ''), True)
				if result != '':
					yield from client.send_message(message.channel, result)
			elif message.content.startswith('!fobot dice '):
				number = message.content.replace('!fobot dice ', '')
				try:
					numberint = int(number)
					if numberint > 0:
						yield from client.send_message(message.channel, 'Your ' + str(numberint) + " sided dice threw a " + str(random.randrange(1, numberint + 1, 1)))
					else:
						yield from client.send_message(message.channel, 'Please use a positive whole number > 0.')
				except ValueError:
					yield from client.send_message(message.channel, 'Please use a positive whole number > 0.')
#			elif message.content.startswith('!fobot follow '):
#				yield from client.send_message(message.channel, 'TODO')
#			elif message.content.startswith('!fobot unfollow '):
#				yield from client.send_message(message.channel, 'TODO')
			elif message.content == '!fobot':
				yield from client.send_message(message.channel, '**Liquipedia** is awesome! Use !fobot help to see the manual.')
			elif message.content == '!fobot mute':
				muted = True
				yield from client.send_message(message.channel, '*Bot is muted now!*')
		if message.content == '!fobot unmute':
			muted = False
			yield from client.send_message(message.channel, '*Bot is unmuted now!*')
		elif message.content.startswith('!fobot addrole '):
			roleid = name=message.content.replace('!fobot addrole ', '')
			if roleid in botroles:
				rolename = botroles[roleid]
				role = discord.utils.get(message.server.roles, name=rolename)
				if hasattr(message.author, 'roles'):
					yield from client.add_roles(message.author, role)
					yield from client.send_message(message.channel, '**Success**: Role added')
				else:
					yield from client.send_message(message.channel, '**Error**: You can\'t add that role')
			else:
				yield from client.send_message(message.channel, '**Error**: You can\'t add that role')
		elif message.content.startswith('!fobot removerole '):
			roleid = name=message.content.replace('!fobot removerole ', '')
			if roleid in botroles:
				rolename = botroles[roleid]
				role = discord.utils.get(message.server.roles, name=rolename)
				if hasattr(message.author, 'roles'):
					yield from client.remove_roles(message.author, role)
					yield from client.send_message(message.channel, '**Success**: Role removed')
				else:
					yield from client.send_message(message.channel, '**Error**: You can\'t remove that role')
			else:
				yield from client.send_message(message.channel, '**Error**: You can\'t remove that role')
	if timestamp + (2 * 3600) < round(time.time()):
		timestamp = round(time.time())
		wiki = wikis[random.randrange(0, len(wikis), 1)]
		channels = message.server.channels
		channel = discord.utils.get(channels, name=wiki)
		if channel != None:
			type = random.randrange(0, 2, 1)
			if type == 0:	
				result = pendingchanges(wiki, False)
				if result != '':
					yield from client.send_message(channel, result)
			elif type == 1:	
				result = unreviewedpages(wiki, False)
				if result != '':
					yield from client.send_message(channel, result)

client.run('token')
