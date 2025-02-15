from __future__ import annotations

import json
import typing

import discord
from discord.ext import commands
from loguru import logger

from config import get_config

if typing.TYPE_CHECKING:
    from jainy_bot import JainyBot

roles_file = get_config('JAINY_BOT_ROLES_FILE')

def load_roles() -> dict:
    logger.info(f'Loading roles from {roles_file}')
    with open(roles_file) as f:
        return json.load(f)


def save_roles(roles: dict) -> None:
    with open(roles_file, 'w') as f:
        json.dump(roles, f, indent=4)
        logger.info(f'Saved roles to {roles_file}')


class Role(commands.Cog, name="Role"):
    def __init__(self, bot: JainyBot):
        self.bot = bot

    @staticmethod
    async def _send_and_raise_role_error(ctx: commands.Context, error_msg: str):
        logger.error(error_msg)
        await ctx.send(error_msg)
        raise commands.BadArgument(error_msg)

    @commands.command()
    async def refresh_role(self, ctx: commands.Context):
        """
        Refreshes the roles that can be asssigned via reaction
        :param ctx:
        :return: None
        """
        try:
            self.bot.reload_react_roles()
            await self.bot.create_react_role_msg(ctx)
        except Exception as e:
            logger.error(f'Failed to reload react roles: {e}')
            await ctx.send('Failed to reload react roles')

        await ctx.send(f'Successfully reloaded react roles')

    @commands.command()
    async def add_role(self, ctx: commands.Context, role: discord.Role, emoji: str, *role_name: str):
        """
        Ties a role to a reaction emoji
        :param role_name: role name for display this will be any text after the emoji in user message
        :param ctx: discord context of the message sent
        :param role: discord role pinged to assign react emoji to
        :param emoji: reaction emoji for role assignment
        :return: None
        """

        logger.info(f'Attempting to add {emoji} to {role}')
        current_roles_lookup = self.bot.emoji_roles_lookup
        current_roles = {r['role_id'] for r in current_roles_lookup.values()}

        error_msg = None
        if emoji in current_roles_lookup:
            error_msg = f'Role {emoji} already assigned to {role}!'
        if role.id in current_roles:
            error_msg = f'Role {role.name} already assigned to an emoji!'

        if error_msg:
            await self._send_and_raise_role_error(ctx, error_msg)

        current_roles_lookup[emoji] = {'role_id': role.id, 'role_name': ' '.join(role_name)}

        save_roles(current_roles_lookup)
        self.bot.reload_react_roles()
