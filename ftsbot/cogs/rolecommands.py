#!/usr/bin/env python3

# License MIT
# Copyright 2016-2022 Alex Winkler
# Version 4.0.0

import math
import discord
from dislash import *
from discord.ext import commands
from ftsbot import config, data
from ftsbot.functions import rolefunctions

class rolecommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@slash_commands.command(description='Get your Discord ID')
	async def discordid(self, ctx):
		await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='User "' + ctx.author.name + '" has ID "' + str(ctx.author.id) + '"'))

	@slash_commands.command(description='Get your wiki roles', guild_ids=config.guild_ids)
	async def wikiroles(self, ctx):
		apidata = rolefunctions.wikiroles(ctx.author.id)
		if apidata == False:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='**Error**: Could not find user with ID "' + str(ctx.author.id) + '" on wiki'))
		else:
			wikigroups = apidata[0]
			silverplus = apidata[1]
			for roleid in wikigroups:
				if roleid in data.wikiroles:
					rolename = data.wikiroles[roleid]
					role = discord.utils.get(ctx.guild.roles, name=rolename)
					if role is not None:
						if roleid == 'editor':
							await ctx.author.add_roles(role)
						elif roleid == 'reviewer':
							await ctx.author.add_roles(role)
			if silverplus == 1:
				role = discord.utils.get(ctx.guild.roles, name='Silver Plus')
				if role is not None:
					await ctx.author.add_roles(role)
			message = await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='**Success**: Wiki Roles added to "' + ctx.author.name + '"'))
			await message.delete(delay=30)

	@slash_commands.is_owner()
	@slash_commands.command(description='Form setup (admin only)', guild_ids=config.guild_ids)
	async def setup(self, ctx):
		# Clean up channel
		async for message in ctx.channel.history():
			await message.delete()

		# Build menu
		entries_per_select = 25

		# Add roles
		c = 0
		# Wikis
		amount_select = math.ceil(len(data.botroleswikis) / entries_per_select)
		components = []
		for i in range(0, amount_select):
			c += 1
			options = []
			for j in range(0, entries_per_select):
				entry_id = j + i * entries_per_select
				if entry_id < len(data.botroleswikis):
					role = data.botroleswikis[entry_id]
					options.append(SelectOption(role, role))
			components.append(SelectMenu(
				custom_id='addrole_select_' + str(c),
				placeholder='Choose which wiki roles you want to add',
				max_values=len(options),
				options=options
			))
		await ctx.send(
			'**Which wiki roles do you want to add?**',
			components=components
		)
		# Languages
		amount_select = math.ceil(len(data.botroleslanguages) / entries_per_select)
		components = []
		for i in range(0, amount_select):
			c += 1
			options = []
			for j in range(0, entries_per_select):
				entry_id = j + i * entries_per_select
				if entry_id < len(data.botroleslanguages):
					role = data.botroleslanguages[entry_id]
					options.append(SelectOption(role, role))
			components.append(SelectMenu(
				custom_id='addrole_select_' + str(c),
				placeholder='Choose which language roles you want to add',
				max_values=len(options),
				options=options
			))
		await ctx.send(
			'**Which language roles do you want to add?**',
			components=components
		)
		# Misc
		amount_select = math.ceil(len(data.botrolesmisc) / entries_per_select)
		components = []
		for i in range(0, amount_select):
			c += 1
			options = []
			for j in range(0, entries_per_select):
				entry_id = j + i * entries_per_select
				if entry_id < len(data.botrolesmisc):
					role = data.botrolesmisc[entry_id]
					options.append(SelectOption(role, role))
			components.append(SelectMenu(
				custom_id='addrole_select_' + str(c),
				placeholder='Choose which misc roles you want to add',
				max_values=len(options),
				options=options
			))
		await ctx.send(
			'**Which misc roles do you want to add?**',
			components=components
		)

		# Remove roles
		c = 0
		# Wikis
		amount_select = math.ceil(len(data.botroleswikis) / entries_per_select)
		components = []
		for i in range(0, amount_select):
			c += 1
			options = []
			for j in range(0, entries_per_select):
				entry_id = j + i * entries_per_select
				if entry_id < len(data.botroleswikis):
					role = data.botroleswikis[entry_id]
					options.append(SelectOption(role, role))
			components.append(SelectMenu(
				custom_id='removerole_select_' + str(c),
				placeholder='Choose which wiki roles you want to remove',
				max_values=len(options),
				options=options
			))
		await ctx.send(
			'**Which wiki roles do you want to remove?**',
			components=components
		)
		# Languages
		amount_select = math.ceil(len(data.botroleslanguages) / entries_per_select)
		components = []
		for i in range(0, amount_select):
			c += 1
			options = []
			for j in range(0, entries_per_select):
				entry_id = j + i * entries_per_select
				if entry_id < len(data.botroleslanguages):
					role = data.botroleslanguages[entry_id]
					options.append(SelectOption(role, role))
			components.append(SelectMenu(
				custom_id='removerole_select_' + str(c),
				placeholder='Choose which language roles you want to remove',
				max_values=len(options),
				options=options
			))
		await ctx.send(
			'**Which language roles do you want to remove?**',
			components=components
		)
		# Misc
		amount_select = math.ceil(len(data.botrolesmisc) / entries_per_select)
		components = []
		for i in range(0, amount_select):
			c += 1
			options = []
			for j in range(0, entries_per_select):
				entry_id = j + i * entries_per_select
				if entry_id < len(data.botrolesmisc):
					role = data.botrolesmisc[entry_id]
					options.append(SelectOption(role, role))
			components.append(SelectMenu(
				custom_id='removerole_select_' + str(c),
				placeholder='Choose which misc roles you want to remove',
				max_values=len(options),
				options=options
			))
		await ctx.send(
			'**Which misc roles do you want to remove?**',
			components=components
		)

	@commands.Cog.listener()
	async def on_slash_command_error(self, ctx, error):
		await ctx.reply(embed=discord.Embed(colour=discord.Colour(0xff0000), description='Forbidden!'))
		print(error)


	@commands.Cog.listener()
	async def on_dropdown(self, ctx):
		dropdowntype = None
		if ctx.component.custom_id.startswith('addrole_select_'):
			dropdowntype = 'addrole'
		elif ctx.component.custom_id.startswith('removerole_select_'):
			dropdowntype = 'removerole'

		if dropdowntype in ['addrole', 'removerole']:
			for option in ctx.component.selected_options:
				if option.value in data.botroleswikis or option.value in data.botroleslanguages or option.value in data.botrolesmisc:
					role = discord.utils.get(ctx.guild.roles, name=option.value)
					if role is not None:
						if dropdowntype == 'addrole':
							await ctx.author.add_roles(role)
							message = await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='**Success**: Role "' + role.name + '" added to "' + ctx.author.name + '"'))
							await message.delete(delay=30)
						elif dropdowntype == 'removerole':
							await ctx.author.remove_roles(role)
							message = await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='**Success**: Role "' + role.name + '" removed from "' + ctx.author.name + '"'))
							await message.delete(delay=30)
				else:
					message = await ctx.send(embed=discord.Embed(colour=discord.Colour(0xff0000), description='**Error**: Dear ' + ctx.author.name + ', "' + option.value + '" is not a valid role "' + ctx.author.name + '"'))
					await message.delete(delay=30)
