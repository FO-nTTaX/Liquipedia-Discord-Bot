# -*- coding: utf-8 -*-

# License MIT
# Copyright 2016-2018 Alex Winkler
# Version 2.0.4

import discordbottoken
import discord
import random
import requests
import json
import time
import datetime
import urllib
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '!fobot ', intents=intents)
client = bot

muted = False
game = discord.Game(name='Liquipedia', url='https://liquipedia.net', type=1)

wikibaseurl = 'https://liquipedia.net/'
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
	'clashroyale',
	'crossfire',
	'battlerite',
	'trackmania',
	'teamfortress',
	'leagueoflegends',
	'worldofwarcraft',
	'fifa',
	'pokemon',
	'arenafps',
	'rainbowsix',
	'pubg',
	'artifact',
	'paladins',
	'battalion',
	'fortnite',
	'arenaofvalor',
	'criticalops',
	'magic',
	'callofduty',
	'apexlegends',
	'autochess',
	'simracing',
	'underlords',
	'teamfighttactics',
	'brawlstars',
	'runeterra',
	'valorant',
	'freefire',
	'ageofempires',
	'wildrift',
	'squadrons'
]
botroles = {
	# wikis
	'bw': 'Starcraft',
	'broodwar': 'Starcraft',
	'sc': 'Starcraft',
	'starcraft': 'Starcraft',
	'starcraftbroodwar': 'Starcraft',
	'sc2': 'Starcraft 2',
	'starcraft2': 'Starcraft 2',
	'starcraftii': 'Starcraft 2',
	'dota': 'Dota 2',
	'dota2': 'Dota 2',
	'hs': 'Hearthstone',
	'hearthstone': 'Hearthstone',
	'hots': 'Heroes',
	'heroes': 'Heroes',
	'heroesofthestorm': 'Heroes',
	'smash': 'Smash',
	'ssb' : 'Smash',
	'ssbm' : 'Smash',
	'sm4sh' : 'Smash',
	'ssb4' : 'Smash',
	'smash64' : 'Smash',
	'projectm' : 'Smash',
	'pm' : 'Smash',
	'cs': 'Counter-Strike',
	'csgo': 'Counter-Strike',
	'counterstrike': 'Counter-Strike',
	'counterstrikeglobaloffensive': 'Counter-Strike',
	'counterstrike:globaloffensive': 'Counter-Strike',
	'ow': 'Overwatch',
	'overwatch': 'Overwatch',
	'war3': 'Warcraft',
	'wc3': 'Warcraft',
	'warcraft3': 'Warcraft',
	'warcraft': 'Warcraft',
	'fgc': 'Fighters',
	'fighters': 'Fighters',
	'streetfighter': 'Fighters',
	'rl': 'Rocket League',
	'rocketleague': 'Rocket League',
	'clash': 'Clash Royale',
	'clashroyale': 'Clash Royale',
	'crossfire': 'CrossFire',
	'battlerite': 'Battlerite',
	'trackmania': 'TrackMania',
	'tf': 'Team Fortress',
	'tf2': 'Team Fortress',
	'teamfortress': 'Team Fortress',
	'teamfortress2': 'Team Fortress',
	'lol': 'League of Legends',
	'leagueoflegends': 'League of Legends',
	'wow': 'World of Warcraft',
	'worldofwarcraft': 'World of Warcraft',
	'pokemon': 'Pokémon',
	'pokémon': 'Pokémon',
	'dbt': 'Arena FPS',
	'diabotical': 'Arena FPS',
	'qc': 'Arena FPS',
	'quake': 'Arena FPS',
	'quakechampions': 'Arena FPS',
	'arenafps': 'Arena FPS',
	'fifa': 'FIFA',
	'r6': 'Rainbow Six',
	'r6s': 'Rainbow Six',
	'rainbow6': 'Rainbow Six',
	'rainbow6siege': 'Rainbow Six',
	'rainbowsix': 'Rainbow Six',
	'rainbowsixsiege': 'Rainbow Six',
	'siege': 'Rainbow Six',
	'bgmi': 'PUBG',
	'pubg': 'PUBG',
	'pubgm': 'PUBG',
	'pubgmobile': 'PUBG',
	'artifact': 'Artifact',
	'paladins': 'Paladins',
	'battalion': 'Battalion',
	'battalion1944': 'Battalion',
	'fortnite': 'Fortnite',
	'arenaofvalor': 'Arena of Valor',
	'criticalops': 'Critical Ops',
	'callofduty': 'Call of Duty',
	'cod': 'Call of Duty',
	'callofdutymobile': 'Call of Duty',
	'codm': 'Call of Duty',
	'codmobile': 'Call of Duty',
	'magic': 'Magic',
	'mtg': 'Magic',
	'magicthegathering': 'Magic',
	'apex': 'Apex Legends',
	'apexlegends': 'Apex Legends',
	'autochess': 'Auto Chess',
	'simracing': 'Sim Racing',
	'racing': 'Sim Racing',
	'underlords': 'Underlords',
	'dotaunderlords': 'Underlords',
	'dota2underlords': 'Underlords',
	'tft': 'Teamfight Tactics',
	'teamfighttactics': 'Teamfight Tactics',
	'brawlstars': 'Brawl Stars',
	'runeterra': 'Runeterra',
	'legendsofruneterra': 'Runeterra',
	'valorant': 'VALORANT',
	'freefire': 'Free Fire',
	'ageofempires': 'Age of Empires',
	'ageofempires2': 'Age of Empires',
	'aoe': 'Age of Empires',
	'aoe2': 'Age of Empires',
	'wildrift': 'Wild Rift',
	# Common(s)
	'commons': 'Commons',
	'templates': 'Templates',
	# Languages
	'japan' : 'Japanese',
	'japanese' : 'Japanese',
	'chinese' : 'Chinese (Mandarin)',
	'china' : 'Chinese (Mandarin)',
	'mandarin' : 'Chinese (Mandarin)',
	'russia' : 'Russian',
	'russian' : 'Russian',
	'spain' : 'Spanish',
	'spanish' : 'Spanish',
	'portugal' : 'Portuguese',
	'portuguese' : 'Portuguese',
	'germany' : 'German',
	'german' : 'German',
	'baguette' : 'French',
	'french' : 'French',
	'france' : 'French',
	'italy' : 'Italian',
	'italian' : 'Italian',
	'thai' : 'Thai',
	'thailand' : 'Thai',
	'hindi' : 'Hindi',
	'denmark' : 'Danish',
	'danish' : 'Danish',
	'swedish' : 'Swedish',
	'sweden' : 'Swedish',
	'tagalog' : 'Tagalog',
	'polish' : 'Polish',
	'poland' : 'Polish',
	'norwegian' : 'Norwegian',
	'norway' : 'Norwegian',
	'ukrainian' : 'Ukrainian',
	'ukraine' : 'Ukrainian',
	'serbia' : 'Serbian',
	'serbian' : 'Serbian',
	'belarusian' : 'Belarusian',
	'belarus' : 'Belarusian',
	'bulgaria' : 'Bulgarian',
	'bulgarian' : 'Bulgarian',
	'macedonian' : 'Macedonian',
	'macedonian' : 'Macedonian',
	'czech' : 'Czech',
	'czechia' : 'Czech',
	'slovak' : 'Slovak',
	'slovakia' : 'Slovak',
	'slovene' : 'Slovene',
	'slovenia' : 'Slovene',
	'croatian' : 'Croatian',
	'croatia' : 'Croatian',
	'bosnian'  : 'Bosnian',
	'bosnia' : 'Bosnian',
	'arabic' : 'Arabic',
	'hungarian' : 'Hungarian',
	'hungaria' : 'Hungarian',
	'korean' : 'Korean',
	'korea' : 'Korean',
	'english' : 'English (native)',
	'american' : 'English (native)',
	'england' : 'English (native)',
	# Misc
	'cspredictions': 'CS Predictions',
	'gamenight': 'Game Night',
	'announcements': 'Announcements',
	'randomstats': 'Random Stats of the Day',
	'randomstatsoftheday': 'Random Stats of the Day'
}
sbotroles = {
	'randomstats': 'Random Stats of the Day',
	'randomstatsoftheday': 'Random Stats of the Day'
}
wikiroles = {
	'editor': 'Editor',
	'reviewer': 'Reviewer'
}
reactionspammers=[]
countchannelmessagemax = 100
countchannelmessage = {}
for wiki in wikis:
	countchannelmessage[wiki] = 0
lies = [
	'Liquipedia is not awesome... (good that this is a lie ^^)',
	'salle is a young girl',
	'Pizza is bad and no one likes it',
	'salle\'s ideas are always realistic',
	'Chrome is a decent browser',
	'blame swampflare',
	'The revision system of Liquipedia is useless, just kill the history',
	'I played Half Life 3 recently, it sucked',
	'WarCraft 4 is just about to be released',
	'Dota 2 is so tiny, we should focus on big esports like Nokia Snake instead',
	'https://files.catbox.moe/o8tify.gif',
	'Swampflare never laundered memory in his Lithuanian bakery!',
]

def lie():
	global lies
	i = random.randrange(0, len(lies), 1)
	return lies[i]

def pendingchanges(wiki, displaynochanges):
	global wikibaseurl
	global wikis
	global countchannelmessage
	global countchannelmessagemax
	result = ''
	if wiki in wikis:
		if countchannelmessage[wiki] >= countchannelmessagemax or displaynochanges:
			countchannelmessage[wiki] = 0
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
				result = '**[Pages with pending changes](' + wikibaseurl + wiki + '/Special:PendingChanges)**: (' + countstr + ' page' + plural + ' pending)'
				for i in range(0, min(count, 5)):
					result += '\n- [' + results[i]['title'] + '](' + wikibaseurl + wiki + '/' + urllib.parse.quote(results[i]['title'].replace(' ', '_')) + ') (diff: ' + str(results[i]['diff_size']) + ', since: ' + results[i]['pending_since'][0:10] + ')'
	else:
		result = wikibaseurl + wiki + ' is not a wiki url we have!'
	return result

def unreviewedpages(wiki, displaynochanges):
	global wikibaseurl
	global wikis
	global countchannelmessage
	global countchannelmessagemax
	result = ''
	if wiki in wikis:
		if countchannelmessage[wiki] >= countchannelmessagemax or displaynochanges:
			countchannelmessage[wiki] = 0
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
				result = '**[Unreviewed pages](' + wikibaseurl + wiki + '/Special:UnreviewedPages)**: (' + countstr + ' page' + plural + ' unreviewed)'
				for i in range(0, min(count, 5)):
					result += '\n- [' + results[i]['title'] + '](' + wikibaseurl + wiki + '/' + urllib.parse.quote(results[i]['title'].replace(' ', '_')) + ')'
	else:
		result = wikibaseurl + wiki + ' is not a wiki url we have!'
	return result

def search(wiki, searchstring):
	global wikibaseurl
	global wikis
	global countchannelmessage
	global countchannelmessagemax
	result = ''
	if wiki in wikis:
		countchannelmessage[wiki] = 0
		url = wikibaseurl + wiki + '/api.php?action=query&format=json&list=search&srlimit=5&srsearch=' + searchstring
		jsonobj = requests.get(url).json()
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
			result = '**[Search results](' + wikibaseurl + wiki + '/index.php?title=Special%3ASearch&profile=default&search=' + searchstring.replace(' ', '+') + '&fulltext=Search)**: (' + countstr + ' page' + plural + ')'
			for i in range(0, min(count, 5)):
				result += '\n- [' + results[i]['title'] + '](' + wikibaseurl + wiki + '/' + urllib.parse.quote(results[i]['title'].replace(' ', '_')) + ')'
	else:
		result = wikibaseurl + wiki + ' is not a wiki url we have!'
	return result

def getwikiroles(discordid):
	global wikibaseurl
	url = wikibaseurl + 'commons/api.php?format=json&action=teamliquidintegration-discordids'
	payload = {
		'discordid': discordid,
		'apikey': discordbottoken.apikey
	}
	jsonobj = requests.post(url, data=payload).json()
	if 'error' in jsonobj:
		return False
	else:
		return [jsonobj['teamliquidintegration-discordids']['groups'],jsonobj['teamliquidintegration-discordids']['silverplus']]

def die(sides): #My sides are killing me
	try:
		s = int(sides)
		if s > 0:
			result = 'Your ' + str(s) + '-sided die threw a ' + str(random.randrange(1, s + 1, 1)) + '.'
		else:
			result = 'Please use a positive whole number > 0.'
	except ValueError:
		result = 'Please use a positive whole number > 0.'
	return result

def dice(sides, count=1):
	try:
		s = int(sides)
		c = int(count)
		if s > 0:
			if c == 1:
				result = die(s)
			elif c > 1:
				rolls = [random.randrange(1, s + 1, 1) for _ in range(c)]
				result = 'Your ' + str(c) + ' ' + str(s) + '-sided dice threw ' + str(rolls) + ' for a total of ' + str(sum(rolls)) + '.'
			else:
				result = 'Please use two positive whole numbers > 0.'
		else:
			result = 'Please use two positive whole numbers > 0.'
	except ValueError:
		result = 'Please use two positive whole numbers > 0.'
	return result

def check_blacklisted(msg):
	for phrase in blacklisted:
		if phrase in msg: return True

@client.event
async def on_ready():
	global game
	await client.change_presence(activity=game)
	while True:
		await asyncio.sleep(60)#sets the time after which the reaction spamm list is cleared
		reactionspammers.clear()

@client.event
async def on_member_join(member):
	#check if user account was created within last day
	if (datetime.datetime.utcnow() - member.created_at).days <= 1:
		role = discord.utils.get(member.guild.roles, name="Muted")
		await member.add_roles(role)
                
@client.event
async def on_reaction_add(reaction, user):
	#check if user joind within last 7 days
	if (datetime.datetime.utcnow() - user.joined_at).days <= 7:
		counter = 1
		#count reactions of that user within the last 60 second intervall (time defined above in on_ready event)
		for id in reactionspammers:
			if id == user.id: counter+=1
		reactionspammers.append(user.id)
		#take action if > 5 reactions were made in the last 60 second intervall (time defined above in on_ready event)
		if counter > 5:
			await reaction.message.guild.ban(user, reason="automated ban, reaction spam")
                        
@client.event
async def on_message(message):
	global muted
	global countchannelmessage
	global countchannelmessagemax
	global botroles
	global sbotroles
	global wikiroles
	global wikis
	if (len(message.role_mentions) + len(message.mentions)) >= 5:
		if (datetime.datetime.utcnow() - message.author.joined_at).days <= 7:
			await message.guild.ban(message.author, reason="automated ban, mass ping")
	if message.channel.name in wikis:
		countchannelmessage[message.channel.name] += 1
	if message.content == '!fobot' or message.content.startswith('!fobot'):
		if not muted:
			if message.content == '!fobot liquipedia':
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='**Liquipedia** is awesome! Use !fobot help to see the manual.'))
			elif message.content == '!fobot guides':
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='**Liquipedia-Guides**: https://liquipedia.net/starcraft2/User:FO-BoT#Guides'))
			elif message.content == '!fobot hype':
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x663399), description='**\\\\Ü/ HYPE \\\\Ü/**'))
				await message.channel.send('https://i.imgur.com/xmdBFq9.mp4')
			elif message.content == '!fobot todo':
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='**Liquipedia-To Do Lists**: https://liquipedia.net/starcraft2/User:FO-BoT#To_Do_Lists'))
			elif message.content == '!fobot dance':
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x663399), description='**EVERYBODY DANCE \\\\Ü/**\n*dances :D\\\\-<*\n*dances :D|-<*\n*dances :D/-<*'))
			elif message.content == '!fobot help':
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='**FO-BoT Commands**: https://liquipedia.net/starcraft2/User:FO-BoT#Manual'))
			elif message.content == '!fobot lie':
				response = lie()
				if '.' in response:
					await message.channel.send(response)
				else:
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x663399), description=response))
			elif message.content.startswith('!fobot talk ') and message.guild == None and message.author.id == '138719439834185728':
				await message.channel.send('Hello ' + message.author.name)
			elif message.content == '!fobot coder':
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x663399), description='FO-BoT was coded by **FO-nTTaX**'))
			elif message.content == '!fobot ranking':
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='**Liquipedia ranking**: https://liquipedia.net/statistics/'))
			elif message.content == '!fobot thinking':
				await message.channel.send('https://files.catbox.moe/o8tify.gif')
			elif message.content == '!fobot brutal savage rekt':
				await message.channel.send('https://thumbs.gfycat.com/NippyKindLangur-mobile.mp4')
			elif message.content == '!fobot blame':
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x663399), description='**#blamesalle**'))
			elif message.content == '!fobot justask':
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='If you need help with something or just have a question, please post the question in the channel for the relevant wiki.' + 
				' Asking if someone can help only costs you extra time, and you usually don\'t even need an admin!'))
			elif message.content == '!fobot lickypiddy':
				lickypiddywiki = 'commons'
				if message.channel.name in wikis:
					lickypiddywiki = message.channel.name
				else:
					lickypiddywiki = 'commons'
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x663399), description='[\\\\Ü/ All glory Lickypiddy \\\\Ü/](https://liquipedia.net/' + lickypiddywiki + '/Special:Lickypiddy)'))
			elif message.content.startswith('!fobot notability'):
				if message.content.replace('!fobot notability ', '') in wikis:
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='[Notability Guidelines](https://liquipedia.net/' + message.content.replace('!fobot notability ', '') + '/Liquipedia:Notability_Guidelines)'))
				elif message.channel.name in wikis:
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='[Notability Guidelines](https://liquipedia.net/' + message.channel.name + '/Liquipedia:Notability_Guidelines)'))
				else:
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='No wiki specified'))
			elif message.content == '!fobot pendingchanges':
				result = pendingchanges(message.channel.name, True)
				if result != '':
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description=result))
			elif message.content.startswith('!fobot pendingchanges '):
				result = pendingchanges(message.content.replace('!fobot pendingchanges ', ''), True)
				if result != '':
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description=result))
			elif message.content == '!fobot unreviewedpages':
				result = unreviewedpages(message.channel.name, True)
				if result != '':
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description=result))
			elif message.content.startswith('!fobot unreviewedpages '):
				result = unreviewedpages(message.content.replace('!fobot unreviewedpages ', ''), True)
				if result != '':
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description=result))
			elif message.content.startswith('!fobot search '):
				result = search(message.channel.name, message.content.replace('!fobot search ', ''))
				if result != '':
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description=result))
			elif message.content.startswith('!fobot die '):
				number = message.content.replace('!fobot die ', '')
				result = die(number)
				if result != '':
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x663399), description=result))
			elif message.content.startswith('!fobot dice '):
				numbers = message.content.replace('!fobot dice ', '').split(' ')
				if len(numbers) == 1:
					swamp = numbers[0].split('d')
					if len(swamp) == 2:
						result = dice(*swamp)
					else:
						result = die(numbers[0])
				elif len(numbers) == 2:
					result = dice(numbers[0], numbers[1])
				else:
					result = 'Please use two positive whole numbers > 0.'
				if result != '':
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x663399), description=result))
			elif message.content == '!fobot':
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='**Liquipedia** is awesome! Use !fobot help to see the manual.'))
			elif message.content == '!fobot mute':
				muted = True
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='*Bot is muted now!*'))
			else: await bot.process_commands(message)
		if message.content == '!fobot unmute':
			muted = False
			await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='*Bot is unmuted now!*'))
		elif message.content == '!fobot discordid':
			await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='User "' + message.author.name + '" has ID "' + str(message.author.id) + '"'))
		elif message.content == '!fobot wikiroles':
			data = getwikiroles(message.author.id)
			if data == False:
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='**Error**: Could not find user with ID "' + str(message.author.id) + '" on wiki'))
			else:
				wikigroups = data[0]
				silverplus = data[1]
				for roleid in wikigroups:
					if roleid in wikiroles:
						rolename = wikiroles[roleid]
						role = discord.utils.get(message.guild.roles, name=rolename)
						if roleid == 'editor':
							await message.author.add_roles(role)
						elif roleid == 'reviewer':
							await message.author.add_roles(role)
				if silverplus == 1:
					role = discord.utils.get(message.guild.roles, name='Silver Plus')
					await message.author.add_roles(role)
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='**Success**: Wiki Roles added to "' + message.author.name + '"'))
		elif message.content.startswith('!fobot addrole '):
			roleid = message.content.replace('!fobot addrole ', '').replace('-', '').replace(' ', '').replace('<', '').replace('>', '').replace(':', '').lower()
			if roleid in botroles:
				rolename = botroles[roleid]
				role = discord.utils.get(message.guild.roles, name=rolename)
				if hasattr(message.author, 'roles'):
					await message.author.add_roles(role)
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='**Success**: Role "' + role.name + '" added to "' + message.author.name + '"'))
				else:
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='**Error**: Can\'t add that role to "' + message.author.name + '"'))
			else:
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='**Error**: Can\'t add that role to "' + message.author.name + '"'))
		elif message.content.startswith('!fobot removerole '):
			roleid = message.content.replace('!fobot removerole ', '').replace('-', '').replace(' ', '').replace('<', '').replace('>', '').replace(':', '').lower()
			if roleid in botroles:
				rolename = botroles[roleid]
				role = discord.utils.get(message.guild.roles, name=rolename)
				if hasattr(message.author, 'roles'):
					await message.author.remove_roles(role)
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='**Success**: Role "' + role.name + '" removed from "' + message.author.name + '"'))
				else:
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='**Error**: Can\'t remove that role from "' + message.author.name + '"'))
			else:
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='**Error**: Can\'t remove that role from "' + message.author.name + '"'))
	elif message.content == '!sallebot' or message.content.startswith('!sallebot'):
		if message.content.startswith('!sallebot addrole '):
			roleid = message.content.replace('!sallebot addrole ', '').replace('-', '').replace(' ', '').replace('<', '').replace('>', '').replace(':', '').lower()
			if roleid in sbotroles:
				rolename = sbotroles[roleid]
				role = discord.utils.get(message.guild.roles, name=rolename)
				if hasattr(message.author, 'roles'):
					await message.author.add_roles(role)
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='Since sallebot is lazy... I added the role for you :P'))
				else:
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='**Error**: Can\'t add that role to "' + message.author.name + '"'))
			else:
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='**Error**: Can\'t add that role to "' + message.author.name + '"'))
		elif message.content.startswith('!sallebot removerole '):
			roleid = message.content.replace('!sallebot removerole ', '').replace('-', '').replace(' ', '').replace('<', '').replace('>', '').replace(':', '').lower()
			if roleid in sbotroles:
				rolename = sbotroles[roleid]
				role = discord.utils.get(message.guild.roles, name=rolename)
				if hasattr(message.author, 'roles'):
					await message.author.remove_roles(role)
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='Since sallebot is lazy... I removed the role for you :P'))
				else:
					await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='**Error**: Can\'t remove that role from "' + message.author.name + '"'))
			else:
				await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='**Error**: Can\'t remove that role from "' + message.author.name + '"'))
	if 'liquidpedia' in message.content.lower():
		await message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='It is **Liquipedia**, only one d in the name! Naughty-counter of ' + message.author.name + ' has been incremented.'))
	if (datetime.datetime.utcnow() - message.author.joined_at).days <= 7:
		for role in message.role_mentions:
			if role.name == 'Liquipedia Admins':
				await message.channel.send('Hello ' + message.author.mention + ', you seem to be new to our server and you have messaged Liquipedia Staff. If your issue is not of private nature, please just write it in the channel for the game it is about.')
	if message.channel.name in wikis:
		if countchannelmessage[message.channel.name] >= countchannelmessagemax:
			if message.channel.name != None:
				type = random.randrange(0, 2, 1)
				if type == 0:
					result = pendingchanges(message.channel.name, False)
					if result != '':
						await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description=result))
				elif type == 1:
					result = unreviewedpages(message.channel.name, False)
					if result != '':
						await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description=result))

@bot.command(
	help='Deletes the specified amount of messages of the specified channel. If no channel is specified it will purge the channel the command was issued in.\nUsage: "!fobot purge <channelname> <amount of messages to be deleted>"',
	brief='Deletes all messages of the specified channel.'
)
async def purge(ctx, channel_name=None, number=100):
	user = ctx.message.author
	if not discord.utils.get(user.roles, name="Admins") and not discord.utils.get(user.roles, name="Liquipedia Staff"):
		await ctx.send('You do not have permission to use this command.')
	else:
		if channel_name == None: channel = ctx.channel
		else: channel = discord.utils.get(ctx.guild.channels, name=channel_name)
		if channel == None: await ctx.send('Invalid channel.')
		await channel.purge(limit=number)

@bot.command(
	help='Creates a temp. private channel and invites the specified user to it.\nUsage: "!fobot create <user>"',
	brief='Creates a temp. private channel and invites the specified user to it.'
)
async def create(ctx, member: discord.Member):
	user = ctx.message.author
	if not discord.utils.get(user.roles, name="Admins") and not discord.utils.get(user.roles, name="Liquipedia Staff"):
		await ctx.send('You do not have permission to use this command.')
	else:
		guild = ctx.message.guild
		admin_role1 = discord.utils.get(guild.roles, name="Admins")
		admin_role2 = discord.utils.get(guild.roles, name="Liquipedia Staff")
		overwrites = {
			guild.default_role: discord.PermissionOverwrite(read_messages=False),
			guild.me: discord.PermissionOverwrite(read_messages=True),
 			admin_role1: discord.PermissionOverwrite(read_messages=True),
			admin_role2: discord.PermissionOverwrite(read_messages=True),
			member: discord.PermissionOverwrite(read_messages=True)
		}
		await guild.create_text_channel('temp_' + member.name, overwrites=overwrites, category=bot.get_channel(int(discordbottoken.privcat)))
		await ctx.send('This channel was created to discuss the private request of ' + member.mention)
		await ctx.message.delete()

@bot.command(
	help='Copies the specified channel (up to 10,000 msgs) to "Private_chat_log". If no channel is specified it will copy the channel the command was issued in. Only works in channels that start with "temp_".\nUsage: "!fobot copy <channelname>"',
	brief='Copies the specified channel to "Private_chat_log".'
)
async def copy(ctx, channel_name=None):
	user = ctx.message.author
	if not discord.utils.get(user.roles, name="Admins") and not discord.utils.get(user.roles, name="Liquipedia Staff"):
		await ctx.send('You do not have permission to use this command.')
	else:
		if channel_name == None: channel = ctx.channel
		else: channel = discord.utils.get(ctx.guild.channels, name=channel_name)
		if channel == None or not channel.name.startswith('temp_'): await ctx.send('Invalid channel.')
		else:
			epmty_array = []
			logtarget = bot.get_channel(discordbottoken.logtarget)
			async for message in channel.history(limit=10000, oldest_first='true'):
				time = message.created_at
				embed = discord.Embed(
					title=message.author.display_name + ' on ' + str(time)[:-7] + ' UTC:',
					color=discord.Color.blue(),
					description=message.content
				)
				await logtarget.send(embed=embed)
				if message.attachments != epmty_array:
				files = message.attachments
				for file in files:
					await logtarget.send(file.url)

@bot.command(
	help='Copies the specified channel to "Private_chat_log" and deletes it thereafter. If no channel is specified it defaults to the channel the command was issued in. Only works in channels that start with "temp_".\nUsage: "!fobot kill_channel <channelname>"',
	brief='Copies the specified channel to "Private_chat_log" and deletes it thereafter.'
)
async def kill_channel(ctx, channel_name=None):
	user = ctx.message.author
	if not discord.utils.get(user.roles, name="Admins") and not discord.utils.get(user.roles, name="Liquipedia Staff"):
		await ctx.send('You do not have permission to use this command.')
	else:
		if channel_name == None: channel = ctx.channel
		else: channel = discord.utils.get(ctx.guild.channels, name=channel_name)
		if channel == None or not channel.name.startswith('temp_'): await ctx.send('Invalid channel.')
		else:
			epmty_array = []
			logtarget = bot.get_channel(discordbottoken.logtarget)
			async for message in channel.history(limit=10000, oldest_first='true'):
				time = message.created_at
				embed = discord.Embed(
					title=message.author.name + ' on ' + str(time)[:-7] + ' UTC:',
					color=discord.Color.blue(),
					description=message.content
				)
				await logtarget.send(embed=embed)
				if message.attachments != epmty_array:
					files = message.attachments
					for file in files:
						await logtarget.send(file.url)
				else:None
			await channel.delete()

#@create.error
async def create_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send('Invalid argument.')
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Please specify an argument.')

bot.run(discordbottoken.token)
