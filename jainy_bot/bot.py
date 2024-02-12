import discord
from discord.ext import commands
from loguru import logger
from config import BOT_PREFIX, BOT_INTENTS, BOT_ROLE_MESSAGE_ID
from .react_roles import emoji_to_role
from jainy_bot.commands import Borb


class JainyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=BOT_PREFIX, intents=BOT_INTENTS, **kwargs)
        self.role_message_id = BOT_ROLE_MESSAGE_ID
        self.emoji_to_role = emoji_to_role
        self.guild = None

    async def setup_hook(self):
        await self.add_cog(Borb(self))

    async def on_ready(self):
        logger.info(f'Logged in as {self.user}')

    def _get_role_by_id(self, role_id: int) -> str:
        return self.guild.get_role(role_id)

    def _is_bad_message(self, payload: discord.RawReactionActionEvent):
        self.guild = self.get_guild(payload.guild_id)
        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            logger.error(f'Invalid Emoji: {payload.emoji}')
            return True

        member = self.guild.get_member(payload.user_id)

        is_missing = payload.message_id != self.role_message_id or self.guild is None or self._get_role_by_id(
            role_id) is None or member is None

        if is_missing:
            return True
        return False

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if self._is_bad_message(payload):
            return
        guild = self.get_guild(payload.guild_id)
        role = guild.get_role(self.emoji_to_role[payload.emoji])

        try:
            await payload.member.add_roles(role)
        except discord.HTTPException:
            logger.error(f'Discord server issue occurred could not connect do discord server: {payload.guild_id}')

        logger.info(
            f'Assigned role = {self._get_role_by_id(self.emoji_to_role[payload.emoji])} to user = {payload.member.name}')

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if self._is_bad_message(payload):
            return

        role_id = self.emoji_to_role[payload.emoji]
        member = self.guild.get_member(payload.user_id)

        try:
            await member.remove_roles(self._get_role_by_id(role_id))
        except discord.HTTPException:
            pass

        logger.info(f'Removed role = {self._get_role_by_id(role_id)} from user = {member.name}')
