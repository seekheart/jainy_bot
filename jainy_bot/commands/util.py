import discord

from datetime import datetime, timezone
from loguru import logger
from discord.ext import commands
from config import BOT_MOD_AUDIT_CHANNEL_ID


def make_general_card(title: str, author: discord.User, thumbnail_url: str | None = None) -> discord.Embed:
    """
    Makes a general discord embed card
    :param title: title of card
    :param author: discord user who triggered the event
    :param thumbnail_url: author's avatar
    :return: discord.Embed object
    """
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
    """
    Makes a discord embed card for moderation events and general server events like invite creation
    :param title: title of card, usually the event
    :param offender: person who is on the receiving end of command usually from kick/ban/unban
    :param moderator: the moderator who performed the action
    :param details: log information about what happened to cause the event
    :return: discord.Embed object
    """
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


async def send_audit_message(guild: discord.Guild, embed: discord.Embed) -> None:
    """
    Sends embed message to audit channel for moderators to view
    :param guild: discord server
    :param embed: the embed message constructed for moderator auditing
    :return: None
    """
    logger.info(f'Sending audit message to guild {guild} channel = {guild.get_channel(BOT_MOD_AUDIT_CHANNEL_ID)}')
    await guild.get_channel(BOT_MOD_AUDIT_CHANNEL_ID).send(embed=embed)


async def send_reply_message(ctx: commands.Context, message: str) -> None:
    """
    Sends reply to user who issued the command and cleans up their last message (usually the command)
    :param ctx: discord context object representing the context of the command call
    :param message: bot reply message
    :return: None
    """
    logger.info(f'Sending reply message to {ctx.author.display_name} in channel {ctx.channel.name}')
    await ctx.send(message)
    try:
        await ctx.message.delete()
    except discord.ext.commands.errors.CommandInvokeError as e:
        logger.warning(f'Original bot command invoked could be deleted')
        logger.error(e)
    except discord.ext.commands.UserNotFound or discord.NotFound as e:
        logger.error(f'User = {ctx.author.display_name} who invoked command is no longer found')
        logger.error(e)
