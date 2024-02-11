import os
import discord

DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

if not DISCORD_BOT_TOKEN:
    raise AttributeError(f'DISCORD_BOT_TOKEN has not been set!')

BOT_PREFIX = os.environ.get('BOT_PREFIX', '$')

BOT_INTENTS = discord.Intents.default()
BOT_INTENTS.members = True
BOT_INTENTS.message_content = True
