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

    @commands.command()
    async def refresh_role(self, ctx: commands.Context):
        """
        Refreshes the roles that can be asssigned via reaction
        :param ctx:
        :return: None
        """
        try:
            self.bot.reload_react_roles()
        except Exception as e:
            logger.error(f'Failed to reload react roles: {e}')
            await ctx.send('Failed to reload react roles')

        await ctx.send(f'Successfully reloaded react roles')

    @commands.command()
    async def add_role(self, ctx: commands.Context, role: discord.Role, em: str):
        """
        Ties a role to a reaction emoji
        :param ctx: discord context of the message sent
        :param role: discord role pinged to assign react emoji to
        :param em: reaction emoji for role assignment
        :return: None
        """

        logger.info(f'Attempting to add {em} to {role}')
        current_roles = self.bot.emoji_roles_lookup

        if em in current_roles:
            error_msg = f'Role {em} already assigned to {role}'
            logger.error(error_msg)
            await ctx.send(error_msg)
            raise commands.BadArgument(error_msg)
