import discord
from discord.ext import commands
from loguru import logger

from config import BOT_PREFIX, BOT_INTENTS, BOT_ROLE_MESSAGE_ID
from jainy_bot.commands import cogs, load_roles, save_roles


class JainyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=BOT_PREFIX, intents=BOT_INTENTS, **kwargs)
        self.role_message_id = BOT_ROLE_MESSAGE_ID
        self.emoji_roles_lookup = load_roles()
        self.guild = None

    def reload_react_roles(self):
        logger.info(f'Reloading react roles')
        self.emoji_roles_lookup = load_roles()
        logger.debug(self.emoji_roles_lookup)

    def save_react_roles(self):
        logger.info(f'Saving react roles')
        save_roles(self.emoji_roles_lookup)

    def _get_role_by_id(self, role_id: int) -> str:
        return self.guild.get_role(role_id)

    async def setup_hook(self):
        for c in cogs:
            logger.info(f"Setting up cog: {c.__name__}")
            await self.add_cog(c(self))

    async def on_ready(self):
        logger.info(f'Logged in as {self.user}')

    def _is_invalid_emoji_role_reaction(self, payload: discord.RawReactionActionEvent):
        self.guild = self.get_guild(payload.guild_id)
        try:
            role_id = self.emoji_roles_lookup[payload.emoji]['role_id']
            logger.info(f'Found role Id = {role_id}')
        except KeyError:
            logger.error(f'Invalid Emoji: {payload.emoji}')
            return True

        member = self.guild.get_member(payload.user_id)

        is_missing = payload.message_id != self.role_message_id or self.guild is None or self._get_role_by_id(
            role_id) is None or member is None

        if is_missing:
            logger.warning(f'invalid emoji role reaction is_missing = {is_missing}')
            logger.debug(f'payload message id = {payload.message_id} role_message_id = {self.role_message_id}')
            logger.debug(f'guild = {self.guild}')
            logger.debug(f'role_id = {self._get_role_by_id(role_id)}')
            logger.debug(f'member = {member}')
            return True
        return False

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if self._is_invalid_emoji_role_reaction(payload):
            logger.error(f"Unrecognized reaction emoji: {payload.emoji}")
            return
        guild = self.get_guild(payload.guild_id)
        role_id = guild.get_role(self.emoji_roles_lookup[payload.emoji]['role_id'])

        logger.info(f'Received reaction add: {payload.emoji}')
        try:
            await payload.member.add_roles(role_id)
        except discord.HTTPException:
            logger.error(f'Discord server issue occurred could not connect do discord server: {payload.guild_id}')

        logger.info(f'Assigned role = {self._get_role_by_id(role_id.id)} to user = {payload.member.name}')

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if self._is_invalid_emoji_role_reaction(payload):
            return

        role_id = self.emoji_roles_lookup[payload.emoji]['role_id']
        member = self.guild.get_member(payload.user_id)

        try:
            await member.remove_roles(self._get_role_by_id(role_id))
        except discord.HTTPException:
            pass

        logger.info(f'Removed role = {self._get_role_by_id(role_id)} from user = {member.name}')
