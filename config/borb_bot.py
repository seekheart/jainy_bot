import discord

from .util import get_config

DISCORD_BOT_TOKEN = get_config(env_var='JAINY_BOT_DISCORD_BOT_TOKEN')
BOT_PREFIX = get_config(env_var='JAINY_BOT_BOT_PREFIX', required=False, default_val='$')
BOT_ROLE_MESSAGE_ID = get_config(env_var='JAINY_BOT_ROLE_MESSAGE_ID', cast_var=int)
BOT_MOD_AUDIT_CHANNEL_ID = get_config('JAINY_BOT_MOD_AUDIT_CHANNEL_ID', cast_var=int)
MODERATOR_ROLES = get_config('JAINY_BOT_MODERATOR_ROLES').split(',')
DEFAULT_GUILD_ID = get_config('JAINY_BOT_DEFAULT_GUILD_ID')
ROLE_ASSIGNMENT_CHANNEL_ID = get_config('JAINY_BOT_ROLE_ASSIGNMENT_CHANNEL_ID', cast_var=int)

BOT_INTENTS = discord.Intents.default()
BOT_INTENTS.members = True
BOT_INTENTS.message_content = True
