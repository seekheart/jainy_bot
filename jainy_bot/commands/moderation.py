from discord.ext import commands
from datetime import datetime, timezone
import discord
from loguru import logger
from config import moderator_roles, BOT_MOD_AUDIT_CHANNEL_ID
from jainy_bot.exceptions import UnauthorizedUserException


def make_general_card(title: str, author: discord.User, thumbnail_url: str | None = None) -> discord.Embed:
    base = discord.Embed(
        title=title,
        timestamp=datetime.now(timezone.utc)
    ).set_author(
        name=author.display_name,
        icon_url=author.avatar.url
    )

    if thumbnail_url:
        base.set_thumbnail(url=thumbnail_url)

    return base


def make_offender_card(title: str, offender: discord.User, moderator: discord.User, details: str) -> discord.Embed:
    return make_general_card(
        title=title,
        author=moderator,
        thumbnail_url=offender.avatar.url
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


async def send_audit_message(guild: discord.Guild, embed: discord.Embed):
    logger.info(f'Sending audit message to guild {guild} channel = {guild.get_channel(BOT_MOD_AUDIT_CHANNEL_ID)}')
    await guild.get_channel(BOT_MOD_AUDIT_CHANNEL_ID).send(embed=embed)


class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.allowed_roles = moderator_roles

    def _is_allowed(self, user_roles: list[discord.Role]):
        for role in user_roles:
            if role.name in self.allowed_roles:
                return True
        return False

    async def _check_if_allowed(self, ctx: commands.Context):
        is_allowed = self._is_allowed(ctx.author.roles)

        if not is_allowed:
            await ctx.send(f'{ctx.author.mention} you are not authorized to use mod commands!')
            logger.error(f'{ctx.author} tried to use mod commands')

            raise UnauthorizedUserException(f'{ctx.author} unauthorized to use mod commands!')
        return True

    @commands.command()
    async def kick(self, ctx: commands.Context, user: discord.User, reason: str):
        """Kicks a user from the server"""
        await self._check_if_allowed(ctx)

        embed = make_offender_card(
            title=f'Kicked user from {ctx.guild.name}',
            offender=user,
            moderator=ctx.author,
            details=reason
        )

        try:
            await ctx.guild.kick(user=user, reason=reason)
        except discord.HTTPException as err:
            logger.error(err.text)
            return await ctx.send(f'could not kick user {user.display_name}')

        await send_audit_message(guild=ctx.guild, embed=embed)

    @commands.command()
    async def ban(self, ctx: commands.Context, user: discord.User, reason: str):
        """Bans a user"""
        await self._check_if_allowed(ctx)

        embed = make_offender_card(
            title=f'Banned user from {ctx.guild.name}',
            offender=user,
            moderator=ctx.author,
            details=reason
        )

        try:
            await ctx.guild.ban(user)
        except discord.HTTPException or discord.Forbidden or discord.NotFound as e:
            logger.error(e.text)
            return await ctx.send(f'Could not ban user {user.display_name}')

        await send_audit_message(guild=ctx.guild, embed=embed)

    @commands.command()
    async def unban(self, ctx: commands.Context, user: discord.User, reason: str):
        """Unbans a user from the server"""
        await self._check_if_allowed(ctx)

        embed = make_offender_card(
            title=f'Unbanned user from {ctx.guild.name}',
            offender=user,
            moderator=ctx.author,
            details=reason
        )

        try:
            await ctx.guild.unban(user)
        except discord.HTTPException or discord.Forbidden or discord.NotFound as e:
            logger.error(e.text)
            return ctx.send(f'Unable to unban user {user.display_name}')

        await send_audit_message(guild=ctx.guild, embed=embed)

    @commands.command()
    async def invite(self, ctx: commands.Context):
        """Creates a one time use invite link"""
        await self._check_if_allowed(ctx)

        embed = make_general_card(
            title=f'{ctx.author.display_name} created invite link',
            author=ctx.author,
            thumbnail_url=ctx.author.avatar.url
        )

        try:
            invite = await ctx.channel.create_invite(
                max_age=1800,
                max_uses=1,
                unique=True,
            )
            embed.add_field(
                name=f'Invite Link',
                value=invite.url,
                inline=False
            ).add_field(
                name=f'Invite created timestamp',
                value=invite.created_at
            ).add_field(
                name=f'Invite expire timestamp',
                value=invite.expires_at
            )
        except discord.HTTPException or discord.Forbidden as e:
            logger.error(e.text)
            return ctx.send(f'Unable to create invite link')

        await ctx.send(invite.url)
        await send_audit_message(guild=ctx.guild, embed=embed)

    @commands.command()
    async def clean(self, ctx: commands.Context, user: discord.Member, num_msg: int):
        """Deletes last N messages by user"""
        await self._check_if_allowed(ctx)
        logger.info(f'Cleaning {num_msg} messages by user = {user.display_name}')

        deleted = []
        async for msg in ctx.channel.history(limit=1000):
            if len(deleted) == num_msg:
                break
            if msg.author == user:
                deleted.append(msg)
                await msg.delete()

        await ctx.send(f'Deleted last {len(deleted)} messages by user = {user.display_name}')
