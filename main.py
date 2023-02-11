import discord
from discord import app_commands
from dotenv import load_dotenv
import os
from typing import Optional
# import members
from pprint import pprint
from discord.ext import commands
import asyncio

# MTAzOTUyMjY5ODYxNjkxMzk0MA.GNRJqz.5LdQdm7R1Pwdc0vAju4jLHwKtRcX24VbstE12I
load_dotenv()
#token = os.getenv('DC_BOT_TOKEN')
token = "MTAzOTUyMjY5ODYxNjkxMzk0MA.GNRJqz.5LdQdm7R1Pwdc0vAju4jLHwKtRcX24VbstE12I"

onehor = discord.Object(id=875740357055352833)
intents = discord.Intents.all()
# client = discord.Client(intents=intents)
# tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix=".", help_command=None, intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    pprint("Connected")
    # try:
    #     synced = await tree.sync(guild=onehor)
    #     pprint(f'Synced {len(synced)} command(s)')
    # except Exception as er:
    #     pprint(er)


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start(token)

asyncio.run(main())
