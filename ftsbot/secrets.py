#!/usr/bin/env python3

# License MIT
# Copyright 2016-2021 Alex Winkler
# Version 3.0.0

token = ''
apikey = ''

with open('.env', 'r') as f:
	for line in f.readlines():
		try:
			key, value = line.split('=')
			locals()[key] = value
		except ValueError:
			# Syntax error
			pass
