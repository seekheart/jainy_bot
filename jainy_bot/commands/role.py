import json

import discord
from discord.ext import commands
from loguru import logger

from config import get_config

roles_file = get_config('JAINY_BOT_ROLES_FILE')


def load_roles() -> dict:
    logger.info(f'Loading roles from {roles_file}')

    roles = {}
    with open(roles_file) as f:
        role_data = json.load(f)

        for r in role_data:
            emo = discord.PartialEmoji.from_str(r['emoji']) if ':' in r['emoji'] else discord.PartialEmoji(
                name=r['emoji'])
            roles[emo] = {
                'role_id': r['role_id'],
                'role_name': r['role_name']
            }

    return roles


def save_roles(roles: dict) -> None:
    save = []
    for k, v in roles.items():
        s = {
            'emoji': k,
            'role_id': v['role_id'],
            'role_name': v['role_name']
        }
        save.append(s)

    with open(roles_file, 'w') as f:
        logger.info(f'Saved roles to {roles_file}')
        json.dump(save, f, indent=4)


class Role(commands.Cog, name="Role"):
    def __init__(self, bot: commands):
        self.bot = bot

    @commands.command()
    async def refresh_role(self, ctx: commands.Context):
        """
        Refreshes the roles that can be asssigned via reaction
        :param ctx:
        :return: None
        """

        self.bot.reload_react_roles()
