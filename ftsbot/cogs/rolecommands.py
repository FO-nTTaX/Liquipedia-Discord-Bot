#!/usr/bin/env python3

# License MIT
# Copyright 2016-2023 Alex Winkler
# Version 4.0.3

import discord
from discord import app_commands
from discord.ext import commands
from ftsbot import data
from ftsbot.functions import autocomplete, rolefunctions


class rolecommands(
	commands.Cog
):
	def __init__(
		self,
		bot
	):
		self.bot = bot

	@app_commands.command(
		description='Get your Discord ID'
	)
	async def discordid(
		self,
		interaction: discord.Interaction
	):
		await interaction.response.send_message(
			embed=discord.Embed(
				colour=discord.Colour(0x00ffff),
				description='User "' + interaction.user.name + '" has ID "' + str(interaction.user.id) + '"'
			)
		)

	@app_commands.command(
		description='Get your wiki roles'
	)
	@app_commands.guild_only()
	async def wikiroles(
		self,
		interaction: discord.Interaction
	):
		apidata = rolefunctions.wikiroles(interaction.user.id)
		if apidata is False:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='**Error**: Could not find user with ID "' + str(interaction.user.id) + '" on wiki'
				)
			)
		else:
			wikigroups = apidata[0]
			silverplus = apidata[1]
			for roleid in wikigroups:
				if roleid in data.wikiroles:
					rolename = data.wikiroles[roleid]
					role = discord.utils.get(interaction.guild.roles, name=rolename)
					if role is not None:
						if roleid == 'editor':
							await interaction.user.add_roles(role)
						elif roleid == 'reviewer':
							await interaction.user.add_roles(role)
			if silverplus == 1:
				role = discord.utils.get(interaction.guild.roles, name='Silver Plus')
				if role is not None:
					await interaction.user.add_roles(role)
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0x00ff00),
					description='**Success**: Wiki Roles added to "' + interaction.user.name + '"'
				)
			)

	@app_commands.command(
		description='Add a role to yourself'
	)
	@app_commands.describe(
		role='Which role do you want to add?',
	)
	@app_commands.guild_only()
	@app_commands.autocomplete(
		role=autocomplete.roles
	)
	async def addrole(
		self,
		interaction: discord.Interaction,
		role: str
	):
		if role not in data.botroles:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='**Error**: Can\'t add that role to "' + interaction.user.name + '"'
				)
			)
		else:
			roleobj = discord.utils.get(interaction.guild.roles, name=role)
			if roleobj is not None:
				try:
					await interaction.user.add_roles(roleobj)
					await interaction.response.send_message(
						embed=discord.Embed(
							colour=discord.Colour(0x00ff00),
							description='**Success**: Role "' + roleobj.name + '" added to "' + interaction.user.name + '"'
						)
					)
				except discord.Forbidden:
					pass

	@app_commands.command(
		description='Remove a role from yourself'
	)
	@app_commands.describe(
		role='Which role do you want to remove?',
	)
	@app_commands.guild_only()
	@app_commands.autocomplete(
		role=autocomplete.roles
	)
	async def removerole(
		self,
		interaction: discord.Interaction,
		role: str
	):
		if role not in data.botroles:
			await interaction.response.send_message(
				embed=discord.Embed(
					colour=discord.Colour(0xff0000),
					description='**Error**: Can\'t remove that role from "' + interaction.user.name + '"'
				)
			)
		else:
			roleobj = discord.utils.get(interaction.guild.roles, name=role)
			if roleobj is not None:
				try:
					await interaction.user.remove_roles(roleobj)
					await interaction.response.send_message(
						embed=discord.Embed(
							colour=discord.Colour(0x00ff00),
							description='**Success**: Role "' + roleobj.name + '" removed from "' + interaction.user.name + '"'
						)
					)
				except discord.Forbidden:
					pass
