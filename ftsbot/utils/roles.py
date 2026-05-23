#!/usr/bin/env python3

from __future__ import annotations

from collections.abc import Collection

import discord


def member_has_any_named_role(member: object, role_names: Collection[str]) -> bool:
	roles = getattr(member, 'roles', None)
	if roles is None:
		return False

	role_name_set = set(role_names)
	return any(getattr(role, 'name', None) in role_name_set for role in roles)


def guild_role_by_name(guild: discord.Guild, role_name: str) -> discord.Role | None:
	return discord.utils.get(guild.roles, name=role_name)
