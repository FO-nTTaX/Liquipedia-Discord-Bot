#!/usr/bin/env python3

# License MIT
# Copyright 2016-2025 Alex Winkler
# Version 4.1.0

import os
envfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')

token = ''
apikey = ''

with open(envfile, 'r') as f:
	for line in f.readlines():
		try:
			key, value = line.split('=')
			locals()[key] = value
		except ValueError:
			# Syntax error
			pass
