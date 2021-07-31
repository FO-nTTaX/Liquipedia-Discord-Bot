#!/usr/bin/env python3

# License MIT
# Copyright 2016-2021 Alex Winkler
# Version 3.0.0

from discord.ext import commands
from dislash import *
from ftsbot import secrets

def is_bot_owner():
	def predicate(ctx):
		if ctx.guild is None:
			return False
		return ctx.author.id == secrets.author
	return check(predicate)
