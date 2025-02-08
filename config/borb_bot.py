import discord

from .util import get_config

DISCORD_BOT_TOKEN = get_config(env_var='DISCORD_BOT_TOKEN')
BOT_PREFIX = get_config(env_var='BOT_PREFIX', required=False, default_val='$')
BOT_ROLE_MESSAGE_ID = get_config(env_var='ROLE_MESSAGE_ID', cast_var=int)
BOT_MOD_AUDIT_CHANNEL_ID = get_config('MOD_AUDIT_CHANNEL_ID', cast_var=int)
MODERATOR_ROLES = get_config('MODERATOR_ROLES').split(',')

BOT_INTENTS = discord.Intents.default()
BOT_INTENTS.members = True
BOT_INTENTS.message_content = True
