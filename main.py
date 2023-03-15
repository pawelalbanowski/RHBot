import discord
from discord import app_commands
from dotenv import load_dotenv
import os
from typing import Optional
# import members
from pprint import pprint
from discord.ext import commands
import asyncio


load_dotenv()
token = os.getenv('DC_BOT_TOKEN')

onehor = discord.Object(id=1077859376414593124)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", help_command=None, intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    pprint("Connected")


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start(token)

asyncio.run(main())
