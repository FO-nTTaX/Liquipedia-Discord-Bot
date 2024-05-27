#!/usr/bin/env python3

# License MIT
# Copyright 2016-2023 Alex Winkler
# Version 4.0.3

wikibaseurl = 'https://liquipedia.net/'

wikis = [
	'ageofempires',
	'apexlegends',
	'arenafps',
	'arenaofvalor',
	'artifact',
	'autochess',
	'battalion',
	'battlerite',
	'brawlhalla',
	'brawlstars',
	'callofduty',
	'clashofclans',
	'clashroyale',
	'commons',
	'counterstrike',
	'criticalops',
	'crossfire',
	'dota2',
	'dota2game',
	'fifa',
	'fighters',
	'fortnite',
	'formula1',
	'freefire',
	'goals',
	'halo',
	'hearthstone',
	'heroes',
	'leagueoflegends',
	'magic',
	'mobilelegends',
	'naraka',
	'omegastrikers',
	'osu',
	'overwatch',
	'paladins',
	'pokemon',
	'pubg',
	'pubgmobile',
	'rainbowsix',
	'rocketleague',
	'runeterra',
	'sideswipe',
	'simracing',
	'smash',
	'smite',
	'splatoon',
	'splitgate',
	'squadrons',
	'starcraft',
	'starcraft2',
	'stormgate',
	'teamfortress',
	'tetris',
	'tft',
	'trackmania',
	'underlords',
	'valorant',
	'warcraft',
	'wildrift',
	'worldoftanks',
	'worldofwarcraft',
	'zula',
]

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
	'A Liquipedia contributor won the first and only The International for Artifact. ' +
		'Their deck had hero cards of 5 different colours.',
]

wikiroles = {
	'editor': 'Editor',
	'reviewer': 'Reviewer'
}

# Roles the bot can add and remove
botroles = [
	'Age of Empires',
	'Apex Legends',
	'Arena FPS',
	'Arena of Valor',
	'Artifact',
	'Auto Chess',
	'Battalion',
	'Battlerite',
	'Brawl Stars',
	'Brawlhalla',
	'Call of Duty',
	'Clash of Clans',
	'Clash Royale',
	'Commons',
	'Counter-Strike',
	'Critical Ops',
	'CrossFire',
	'Dota 2',
	'FIFA',
	'Fighters',
	'Formula 1',
	'Fortnite',
	'Free Fire',
	'GOALS',
	'Halo',
	'Hearthstone',
	'Heroes',
	'League of Legends',
	'Magic',
	'Mobile Legends',
	'Naraka',
	'Omega Strikers',
	'osu',
	'Overwatch',
	'Paladins',
	'Pokémon',
	'PUBG',
	'PUBG Mobile',
	'Rainbow Six',
	'Rocket League',
	'Runeterra',
	'Sim Racing',
	'Smash',
	'SMITE',
	'Splatoon',
	'Splitgate',
	'StarCraft 2',
	'StarCraft',
	'Stormgate',
	'Team Fortress',
	'Teamfight Tactics',
	'Tetris',
	'TrackMania',
	'Underlords',
	'VALORANT',
	'Warcraft',
	'Wild Rift',
	'World of Tanks',
	'World of Warcraft',
	'Zula',

	'Arabic',
	'Belarusian',
	'Bosnian',
	'Bulgarian',
	'Chinese (Mandarin)',
	'Croatian',
	'Czech',
	'Danish',
	'English (native)',
	'French',
	'German',
	'Hindi',
	'Hungarian',
	'Italian',
	'Japanese',
	'Korean',
	'Macedonian',
	'Mongolian',
	'Norwegian',
	'Polish',
	'Portuguese',
	'Russian',
	'Serbian',
	'Slovak',
	'Slovene',
	'Spanish',
	'Swedish',
	'Tagalog',
	'Thai',
	'Turkish',
	'Ukrainian',
	'Vietnamese',

	'Announcements',
	'App Announcements',
	'CS Predictions',
	'Game Night',
	'ML Predictions',
	'Please Ping Me',
	'Random Stats of the Day',
	'R6 Predictions',
	'Templates',
	'VAL Predictions',
]

# Words regularly used in invite spams
bad_words = [
	'nudde',
	'nude',
	'sex',
	's3x',
	'seex',
	'tiktok',
	'18+',
	'kiss',
	'onlyfans',
	'nft',
	'crypto',
]

nitro_spam_triggers = [
	'discord',
	'dissord',
	'discrod',
	'dissrod',
	'free',
	'gift',
	'giveaway',
]
