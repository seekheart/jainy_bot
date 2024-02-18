from datetime import datetime, timedelta
from discord.ext import commands
from loguru import logger


def format_time(t: timedelta) -> str:
    logger.debug(f'Got timedelta = {t}')
    h, m, s = str(t).split(':')
    return f'{h} Hours {m} Minutes {s} Seconds'


class Uptime(commands.Cog, name="Uptime"):
    def __init__(self, bot: commands):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.command()
    async def uptime(self, ctx: commands):
        """Get the uptime for bot"""
        logger.info(f'Generating uptime information')
        delta = datetime.now() - self.start_time
        await ctx.send(f"Uptime: {format_time(delta)}")