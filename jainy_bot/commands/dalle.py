import base64
from io import BytesIO

import aiohttp
import discord
from discord.ext import commands
from loguru import logger

from config import DALLE_API_URL


async def make_api_request(payload: dict) -> dict or None:
    async with aiohttp.ClientSession() as session:
        async with session.post(DALLE_API_URL, json=payload) as response:
            if response.status == 200:
                logger.info(f'Successfully contacted Dalle Api')
                payload = await response.json()
                return payload
            else:
                logger.error(f'Dalle Server responded with status = {response.status}')
                return None


class Dalle(commands.Cog, name="Dalle"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command()
    async def dalle(self, ctx: commands.Context, prompt: str):
        """Create a Dalle generated image with a prompt"""
        logger.info(f"Creating a Dalle image with prompt: {prompt} requested by user {ctx.author}")

        payload = {
            'prompt': prompt
        }

        await ctx.send(f'{ctx.author.mention} hang tight I\'m checking with Dall-E')
        response = await make_api_request(payload)

        if response:
            logger.info(f"Dalle image created successfully")
            await ctx.send(f'{ctx.author.mention} generating image please wait')
            data = response
            images = data['images']
            files = []

            for idx, img in enumerate(images):
                file_bytes = BytesIO(base64.b64decode(img))
                file = discord.File(file_bytes, filename=f"{prompt}_{idx}.jpg")
                files.append(file)

            await ctx.send(
                files=files,
                mention_author=True,
                embed=discord.Embed(title=f'{prompt} requested by {ctx.author}')
            )
        else:
            await ctx.send('Could not generate images')
