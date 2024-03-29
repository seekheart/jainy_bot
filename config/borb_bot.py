import os
import discord

DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

if not DISCORD_BOT_TOKEN:
    raise AttributeError(f'DISCORD_BOT_TOKEN has not been set!')

BOT_PREFIX = os.environ.get('BOT_PREFIX', '$')

BOT_INTENTS = discord.Intents.default()
BOT_INTENTS.members = True
BOT_INTENTS.message_content = True

BOT_ROLE_MESSAGE_ID = int(os.environ.get('ROLE_MESSAGE_ID'))
BOT_MOD_AUDIT_CHANNEL_ID = int(os.environ.get('MOD_AUDIT_CHANNEL_ID'))

if not BOT_ROLE_MESSAGE_ID:
    raise AttributeError(f'BOT_ROLE_MESSAGE_ID cannot be null')
if not BOT_MOD_AUDIT_CHANNEL_ID:
    raise AttributeError(f'BOT_MOD_AUDIT_CHANNEL_ID cannot be null')

MODERATOR_ROLES = os.environ.get('MODERATOR_ROLES').split(',')

if not MODERATOR_ROLES:
    raise AttributeError(f'MODERATOR_ROLES is not set!')