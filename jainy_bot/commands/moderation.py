from discord.ext import commands
from loguru import logger
from config import moderator_roles
from jainy_bot.exceptions import UnauthorizedUserException
from .util import make_general_card, make_offender_card, send_audit_message, send_reply_message
import discord


class Moderation(commands.Cog, name="Moderation"):
    """
    Moderation Cog representing all things moderator
    """

    def __init__(self, bot: commands.bot):
        """
        constructor for the cog to load into the bot when bot calls load_cog
        :param bot: discord bot of interest
        """
        self.bot = bot
        self.allowed_roles = moderator_roles

    def _is_allowed(self, user_roles: list[discord.Role]) -> bool:
        """
        Checks if user is allowed to use this command based on roles
        :param user_roles: list of roles from the user calling the command
        :return: boolean indicating whether user is allowed to use this command
        """
        for role in user_roles:
            if role.name in self.allowed_roles:
                return True
        return False

    async def _check_if_allowed(self, ctx: commands.Context):
        """
        Checks if the caller of the command is allowed to execute command
        :param ctx: discord context of the call
        :return: bool if allowed else raises UnauthorizedUserException
        """
        is_allowed = self._is_allowed(ctx.author.roles)

        if not is_allowed:
            await ctx.send(f'{ctx.author.mention} you are not authorized to use mod commands!')
            logger.error(f'{ctx.author} tried to use mod commands')

            raise UnauthorizedUserException(f'{ctx.author} unauthorized to use mod commands!')
        return True

    @commands.command()
    async def kick(self, ctx: commands.Context, user: discord.User, reason: str) -> None:
        """
        Kicks a user from the server
        :param ctx: discord context of the call
        :param user: user to kick
        :param reason: reason for kicking the user to be logged in audit channel
        :return None
        """
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
            await ctx.send(f'could not kick user {user.display_name}')
            return
        await send_reply_message(ctx, f'kicked user {user.display_name}')
        await send_audit_message(guild=ctx.guild, embed=embed)

    @commands.command()
    async def ban(self, ctx: commands.Context, user: discord.User, reason: str):
        """
        Bans a user from server
        :param ctx: discord calling context
        :param user to kick
        :param reason: reason for banning the user to be logged in audit channel
        :return:
        """
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

        await send_reply_message(ctx, f'banned user {user.display_name}')
        await send_audit_message(guild=ctx.guild, embed=embed)

    @commands.command()
    async def unban(self, ctx: commands.Context, user: discord.User, reason: str):
        """
        Unbans a user from the server
        :param ctx: discord calling context
        :param user: user to unban
        :param reason: reason for unbanning user to be logged in audit channel
        :return:
        """
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

        await send_reply_message(ctx, f'unbanned user {user.display_name}')
        await send_audit_message(guild=ctx.guild, embed=embed)

    @commands.command()
    async def invite(self, ctx: commands.Context) -> None:
        """
        Creates invite one time use invite link set to expire in 30 mins
        :param ctx: discord calling context
        :return: None
        """
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

        await send_reply_message(ctx, f'Invite link created: {invite.url}')
        await send_audit_message(guild=ctx.guild, embed=embed)

    @commands.command()
    async def clean(self, ctx: commands.Context, user: discord.Member, num_msg: int) -> None:
        """
        Cleans up last N messages from user declared in command
        :param ctx: discord calling context
        :param user: user to clean messages from
        :param num_msg: number of messages to delete
        :return: None
        """
        await self._check_if_allowed(ctx)
        logger.info(f'Cleaning {num_msg} messages by user = {user.display_name}')

        deleted = []
        async for msg in ctx.channel.history(limit=1000):
            if len(deleted) == num_msg:
                break
            if msg.author == user:
                deleted.append(msg)
                await msg.delete()

        await send_reply_message(ctx, f'Deleted last {len(deleted)} messages by user = {user.display_name}')
