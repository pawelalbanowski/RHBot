import discord as dc
import os
import pymongo
from dotenv import load_dotenv
from pprint import pprint
from func import process_msg
from admins import Admin
import random


intents = dc.Intents.all()
cli = dc.Client(intents=intents)

load_dotenv()
token = os.getenv('DC_BOT_TOKEN')
mongodb_uri = os.getenv('MONGODB_URI')

mongo = pymongo.MongoClient(mongodb_uri)

# ratio = ['L', 'ratio', 'you fell off', 'never liked u anyway', 'cope', 'seethe',
#         'ur allergic to gluten', "don't care", 'cringe', 'u smell', 'who asked',
#         'stay mad', "didn't ask", 'ur slow']


@cli.event
async def on_ready():
    pprint('connected as {0.user}'.format(cli))


@cli.event
async def on_message(msg):
    # if random.randint(0, 50) == 1:
    #     await msg.reply(ratio[random.randint(0, (len(ratio) - 1))])
    if msg.author == cli.user:
        return

    if msg.channel.id == 1043908550667280535:
        await Admin.toyota_quali(msg)
        await message.add_reaction(":ballot_box_with_check:")

    if msg.content.startswith('.'):
        await process_msg(msg, cli, mongo)
        return

    # elif msg.channel.id == 985977023128281148 and msg.author != cli.user:
    #     roles = list(map((lambda a: a.name), msg.author.roles))
    #     if not ('Admin' in roles or 'Staff' in roles or 'Moderator' in roles):
    #         msg.delete()


cli.run(token)
