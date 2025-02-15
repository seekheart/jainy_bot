from typing import KeysView

import discord
from discord.ext import commands
from loguru import logger

from config import BOT_PREFIX, BOT_INTENTS, DEFAULT_GUILD_ID, ROLE_ASSIGNMENT_CHANNEL_ID
from jainy_bot.commands import cogs, load_roles, save_roles, make_general_card


class JainyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=BOT_PREFIX, intents=BOT_INTENTS, **kwargs)
        self.role_assign_channel_id = ROLE_ASSIGNMENT_CHANNEL_ID
        self.role_assign_msg_id = None
        self.emoji_roles_lookup = load_roles()
        self.guild = DEFAULT_GUILD_ID

    @staticmethod
    async def add_reactions_to_msg(msg: discord.Message, emojis: KeysView[str]):
        for emoji in emojis:
            await msg.add_reaction(discord.PartialEmoji.from_str(emoji))

    async def get_role_assign_msg_id(self) -> int or None:
        """
        Gets the role assignment message id
        :return: an integer representing the role assignment message id if it exists otherwise None
        """
        history = [m async for m in self.get_channel(ROLE_ASSIGNMENT_CHANNEL_ID).history(oldest_first=True, limit=1)]

        if len(history) == 0:
            return None
        return history[0].id

    def _get_role_id_by_emoji(self, emoji: discord.PartialEmoji) -> int:
        emoji_name = emoji.name
        emoji_id = emoji.id

        emoji_custom_name = f'<:{emoji_name}:{emoji_id}>'
        animated_custom_emoji_name = f'<a:{emoji_name}:{emoji_id}>'

        if emoji_name in self.emoji_roles_lookup:
            return self.emoji_roles_lookup[emoji_name]['role_id']
        elif emoji_custom_name in self.emoji_roles_lookup:
            return self.emoji_roles_lookup[emoji_custom_name]['role_id']
        elif animated_custom_emoji_name in self.emoji_roles_lookup:
            return self.emoji_roles_lookup[animated_custom_emoji_name]['role_id']
        else:
            raise KeyError(f'No emoji reaction found for emoji_name = {emoji_name} emoji_id = {emoji_id}')

    async def create_react_role_msg(self, ctx: commands.Context):
        logger.debug(f'Role assignment channel id = {self.role_assign_channel_id}')
        async_history = self.get_channel(self.role_assign_channel_id).history(oldest_first=True)
        logger.debug(f'history = {async_history}')
        prev_msg = [m async for m in async_history]
        prev_msg = prev_msg[0] if len(prev_msg) == 1 else None
        logger.debug(f'Previous message = {prev_msg}')

        if prev_msg:
            logger.info(f'Updating react role message with new roles')
        else:
            logger.info(f'Creating react role message')
            prev_msg = None

        msg_lines = []
        for em, meta_data in self.emoji_roles_lookup.items():
            msg_lines.append(f'{meta_data["role_name"]} = {em}')

        if len(msg_lines) < 1:
            log_msg = f'No reaction role assignments found skipping'
            logger.warning(log_msg)
            await ctx.send(log_msg)
            return

        msg = make_general_card(title='Role Assignment', author=ctx.author)
        msg.add_field(name='Instructions', value=f'React/Un-react to get the desired role assigned', inline=False)
        msg.add_field(name='Roles', value=f'\n'.join(msg_lines), inline=False)

        if prev_msg is not None:
            self.role_assign_msg_id = prev_msg.id
            await prev_msg.edit(embed=msg)
            await self.add_reactions_to_msg(prev_msg, self.emoji_roles_lookup.keys())
        else:
            reply = await self.get_channel(self.role_assign_channel_id).send(embed=msg)
            self.role_assign_msg_id = reply.id
            logger.info(f'Created react role assignment message with channel id = {reply.id}')
            await self.add_reactions_to_msg(reply, self.emoji_roles_lookup.keys())

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
        if self.role_assign_msg_id is None:
            logger.info(f'Setting uo role assignment channel id')
            self.role_assign_msg_id = await self.get_role_assign_msg_id()
            logger.info(f'Successfully setup role assignment channel id')
        logger.info(f'Logged in as {self.user}')

    def _is_invalid_emoji_role_reaction(self, payload: discord.RawReactionActionEvent):
        self.guild = self.get_guild(payload.guild_id)
        if not payload.emoji:
            logger.error(f'No emoji reaction found')
            return True

        try:
            role_id = self._get_role_id_by_emoji(payload.emoji)
            logger.info(f'Found role Id = {role_id}')
        except KeyError:
            logger.error(f'Invalid Emoji: {payload.emoji}')
            return True

        member = self.guild.get_member(payload.user_id)

        is_missing = payload.message_id != self.role_assign_msg_id or self.guild is None or self._get_role_by_id(
            role_id) is None or member is None

        if is_missing:
            logger.warning(f'invalid emoji role reaction is_missing = {is_missing}')
            logger.debug(f'payload message id = {payload.message_id} role_message_id = {self.role_assign_msg_id}')
            logger.debug(f'guild = {self.guild} role_id = {self._get_role_by_id(role_id)} member = {member}')
            return True
        return False

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if self._is_invalid_emoji_role_reaction(payload):
            logger.error(f"Unrecognized reaction emoji: {payload.emoji}")
            return
        guild = self.get_guild(payload.guild_id)
        role_id = guild.get_role(self._get_role_id_by_emoji(payload.emoji))

        logger.info(f'Received reaction add: {payload.emoji}')
        try:
            await payload.member.add_roles(role_id)
        except discord.HTTPException:
            logger.error(f'Discord server issue occurred could not connect do discord server: {payload.guild_id}')

        logger.info(f'Assigned role = {self._get_role_by_id(role_id.id)} to user = {payload.member.name}')

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if self._is_invalid_emoji_role_reaction(payload):
            return

        role_id = self._get_role_id_by_emoji(payload.emoji)
        member = self.guild.get_member(payload.user_id)

        try:
            await member.remove_roles(self._get_role_by_id(role_id))
        except discord.HTTPException:
            pass

        logger.info(f'Removed role = {self._get_role_by_id(role_id)} from user = {member.name}')
