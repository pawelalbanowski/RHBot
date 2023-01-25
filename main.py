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


# @tree.command(name='register', description='Register yourself for 1HoR season 3')
# async def register(msg: discord.Interaction, number: int, gamertag: str, car: str, admin_user: Optional[str]):
#     await msg.response.send_message(embed="helo")


# @tree.command(name='inrole', description='lists members with provided roles', guild=onehor)
# async def inrole(msg: discord.Interaction, role1: str, role2: Optional[str]):
#     response = await members.inrole(client, msg, role1, role2)
#     if response:
#         await msg.response.send_message(embed=response)


# client.run(token)