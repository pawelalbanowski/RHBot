from discord.utils import get
from utils import embed, pages
from pprint import pprint


class Member:
    @staticmethod
    async def inrole(msg, cli):  # .inrole role
        role_str = msg.content.split(' ', 1)[1].strip()
        role_obj = get(msg.guild.roles, name=role_str)
        members_list = []

        if role_obj is None:
            await msg.reply(embed=embed("Role doesn't exist"))

        for member in msg.guild.members:
            if role_obj in member.roles:
                members_list.append(f'{member.name}\n')

        if len(members_list) > 0:
            await pages(cli, msg, members_list)

    @staticmethod
    async def pet(msg):  # .pet
        await msg.reply(f'Fuck you {msg.author.mention}')

    @staticmethod
    async def gnfos(msg):  # .gnfos
        await msg.reply('Good neighbors from our server :pray:')

    @staticmethod
    async def fh5(msg):  # .fh5
        await msg.reply('Forza Horizon 5 is a perfect game with no obvious flaws!')

    @staticmethod
    async def cruise(msg):  # .fh5
        await msg.reply("""Cruise Rules:
    1. No slamming into convoy members.
    2. No racing on cruises.
    3. No drifting on cruises.
    4. Stay on the road and stick with convoy members while cruising.
    5. Hands off controller or pedals while parked!
    6. You must be in stream to participate in Races and Cruising.
    7. No very large vehicles in cruises (Gurkha’s, Unimog’s, etc.) unless those types of vehicles are part of the cruise theme. 
    8. No drag and or drift cars.""")