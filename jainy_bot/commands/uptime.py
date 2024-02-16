from datetime import datetime, timedelta
from discord.ext import commands


def _format_time(t: timedelta) -> str:
    h, m, s = str(t).split(':')
    return f'{h} Hours {m} Minutes {s} Seconds'


class Uptime(commands.Cog, name="Uptime"):
    def __init__(self, bot: commands):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.command()
    async def uptime(self, ctx: commands):
        """Get the uptime for bot"""
        delta = datetime.now() - self.start_time
        await ctx.send(f"Uptime: {_format_time(delta)}")