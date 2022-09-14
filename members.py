from discord.utils import get
from utils import embed, pages, embed_timeout, find_re
from pprint import pprint
import asyncio


class Member:
    @staticmethod
    async def inrole(msg, cli):  # .inrole role or .inrole role, role
        roles = list(map((lambda a: a.name), msg.guild.roles))
        role_str = msg.content.split(' ', 1)[1].strip()
        findrole1 = None
        findrole2 = None
        if ',' in msg.content:
            roles_str = role_str.split(', ', 1)
            findrole1 = find_re(roles, roles_str[0])
            findrole2 = find_re(roles, roles_str[1])
            findrole = None
        else:
            findrole = find_re(roles, role_str)
        if findrole:
            role_obj = get(msg.guild.roles, name=findrole)
            members_list = []

            if role_obj is None:
                await msg.reply(embed=embed("Role doesn't exist"))

            for member in msg.guild.members:
                if role_obj in member.roles:
                    members_list.append(f'{member.name}\n')

            if len(members_list) > 0:
                await pages(cli, msg, members_list, f"**List of users in role: {findrole}**")

        elif findrole1 and findrole2:
            role1_obj = get(msg.guild.roles, name=findrole1)
            role2_obj = get(msg.guild.roles, name=findrole2)
            members_list = []

            for member in msg.guild.members:
                if role1_obj in member.roles and role2_obj in member.roles:
                    members_list.append(f'{member.name}\n')

            if len(members_list) > 0:
                await pages(cli, msg, members_list, f"**List of users in roles: {findrole1}, {findrole2}**")

        else:
            await msg.reply(embed=embed("Role not found or found more than one matching."))

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

    @staticmethod
    async def driver(msg, roles, mongo, cli):  # .driver number or .driver mentions
        db = mongo['Season2']
        drivers_col = db['Drivers']

        if len(msg.mentions) != 0 and ('Admin' in roles or 'Staff' in roles):
            drivers = list(map((lambda a: a.id), msg.mentions))
            key = "id"
        else:
            drivers = msg.content.split(' ', 1)[1].split(' ')
            key = "nr"

        pages_num = len(drivers)
        cur_page = 1

        async def driverinfo(page):
            drivernum = page - 1
            cur_driver = drivers_col.find_one({key: int(drivers[drivernum])})
            if cur_driver is None:
                info = f"Could not find driver"
            else:
                info = f"""Gamertag: {cur_driver['gt']}
                       DC Username: {cur_driver['dcname']}
                       number: {cur_driver['nr']}
                       league: {cur_driver['league']}
                       car: {cur_driver['car']}
                       swaps: {cur_driver['swaps']}"""
            return info

        info = await driverinfo(cur_page)
        message = await msg.reply(embed=embed(f"Page {cur_page}/{pages_num}:\n\n{info}"))

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == msg.author and str(reaction.emoji) in ["◀️", "▶️", '👍']
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await cli.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages_num:
                    cur_page += 1
                    await message.edit(
                        embed=embed(f"PAGE {cur_page}/{pages_num}:\n\n{await driverinfo(cur_page)}"))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(
                        embed=embed(f"PAGE {cur_page}/{pages_num}:\n\n{await driverinfo(cur_page)}"))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == '👍':
                    await message.delete()
                    await msg.delete()

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                await msg.delete()
                break

    @staticmethod
    async def race(msg, mongo, cli):  # .race [number] [league]
        parameters = msg.content.split(' ')
        race_role = get(msg.guild.roles, name=f"{parameters[2].lower().capitalize()} Race {parameters[1]}")
        members_list = f"Gamertags of drivers in Race {parameters[1]} of {parameters[2].lower().capitalize()}:\n\n"
        db = mongo['Season2']
        drivers_col = db['Drivers']

        if race_role is None:
            await msg.reply(embed=embed("Invalid parameters, do .race [number] [league]"))

        for member in msg.guild.members:
            if race_role in member.roles:
                driver = drivers_col.find_one({"id": member.id})
                members_list += f"{driver['gt']}\n"

        if len(members_list) > 0:
            await embed_timeout(cli, msg, embed(members_list), False)

    @staticmethod
    async def clubs(msg, cli):  # .clubs
        roles = list(map((lambda a: a.name), msg.guild.roles))
        clubs = []
        leader_role = get(msg.guild.roles, name="Club Leader")

        for role in roles:
            if "[" in role and "]" in role:
                role_obj = get(msg.guild.roles, name=role)
                club = {
                    "name": role,
                    "leader": "",
                    "members": ""
                }

                for member in msg.guild.members:
                    if role_obj in member.roles and leader_role in member.roles:
                        club["leader"] = member.name
                    elif role_obj in member.roles:
                        club["members"] += f"\n{member.name}"

                clubs.append(club)

        pages_num = len(clubs)
        cur_page = 1
        message = await msg.reply(embed=embed(
            f"Page {cur_page}/{pages_num}:\n**{(clubs[0])['name']}**\n**Leader:** {(clubs[0]['leader'])}\n**Members:**{(clubs[0])['members']}"))

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == msg.author and str(reaction.emoji) in ["◀️", "▶️", '👍']
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await cli.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages_num:
                    cur_page += 1
                    await message.edit(embed=embed(
                        f"Page {cur_page}/{pages_num}:\n**{(clubs[cur_page-1])['name']}**\n**Leader:** {(clubs[cur_page-1]['leader'])}\n**Members:**{(clubs[cur_page-1])['members']}"))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=embed(
                        f"Page {cur_page}/{pages_num}:\n**{(clubs[cur_page-1])['name']}**\n**Leader:** {(clubs[cur_page-1]['leader'])}\n**Members:**{(clubs[cur_page-1])['members']}"))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == '👍':
                    await message.delete()
                    await msg.delete()

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                await msg.delete()
                break
