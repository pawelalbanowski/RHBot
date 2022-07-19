import discord as dc
import os

from dotenv import load_dotenv
from pprint import pprint
from func import process_msg


intents = dc.Intents.all()
cli = dc.Client(intents=intents)

load_dotenv()
token = os.getenv('DC_BOT_TOKEN')
mongodb_uri = os.getenv('MONGODB_URI')


@cli.event
async def on_ready():
    pprint('connected as {0.user}'.format(cli))


@cli.event
async def on_message(msg):
    if msg.author == cli.user:
        return
    if msg.content.startswith('.'):
        await process_msg(msg, cli)

cli.run(token)
