from discord.ext import commands
from datetime import datetime, timezone
import discord
from loguru import logger
from config import moderator_roles, BOT_MOD_AUDIT_CHANNEL_ID


def make_moderation_card(title: str, offender: discord.User, moderator: discord.User, details: str) -> discord.Embed:
    return discord.Embed(
        timestamp=datetime.now(timezone.utc),
        title=f'{title}',
    ).set_thumbnail(
        url=offender.avatar.url
    ).set_author(
        name=moderator.display_name,
        icon_url=moderator.avatar.url
    ).add_field(
        name=f'User Name',
        value=f'{offender.name}'
    ).add_field(
        name=f'User ID',
        value=f'{offender.id}'
    ).add_field(
        name=f'Details',
        value=f'{details}',
        inline=False
    )


class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.allowed_roles = moderator_roles

    def _is_allowed(self, user_roles: list[discord.Role]):
        for role in user_roles:
            if role.name in self.allowed_roles:
                return True
        return False

    @commands.command()
    async def kick(self, ctx: commands.Context, user: discord.User, reason: str):
        """Kicks a user from the server and records the reason why in audit channel"""
        roles = ctx.author.roles
        is_allowed = self._is_allowed(roles)

        if not is_allowed:
            return await ctx.send(f'{ctx.author.mention} you are not authorized to use mod commands!')

        embed = make_moderation_card(
            title=f'Kicked user from {ctx.guild.name}',
            offender=user,
            moderator=ctx.author,
            details=reason
        )
        await ctx.guild.get_channel(BOT_MOD_AUDIT_CHANNEL_ID).send(embed=embed)
        try:
            await ctx.guild.kick(user=user, reason=reason)
        except discord.HTTPException as err:
            logger.error(err.text)
