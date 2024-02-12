from discord.ext import commands


class Borb(commands.Cog, name='Borb'):
    def __init__(self, bot: commands):
        self.bot = bot

    @commands.command()
    async def borb(self, ctx, name):
        """Borb a person"""
        await ctx.send(f'Borbing {name}')

