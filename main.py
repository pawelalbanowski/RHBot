import discord as dc
import os
from pprint import pprint
from func import process_msg
from discord.ext import commands

cli = dc.Client()

token = 'OTYyMzU1OTg1NTU5NzQ4Njc4.Gx0voM.zHvYEI-r-eEN5-VNc28ADqDEGOSiqrTAvmcYj0'


@cli.event
async def on_ready():
    pprint('connected as {0.user}'.format(cli))


@cli.event
async def on_message(msg):
    if msg.author == cli.user:
        return
    if msg.content.startswith('.'):
        await process_msg(msg)

cli.run(token)
