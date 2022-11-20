from discord.utils import get
from json_util import json_read, json_write
from utils import embed, embed_timeout, find_re
from pprint import pprint
from gsheetio import update_gsheet
import discord as dc
from datetime import date
import asyncio


def divide_chunks(content, size):
    for i in range(0, len(content), size):
        yield content[i:i + size]


async def pages(cli, msg, content, title):
    el_count = len(content)
    contents = list(divide_chunks(content, 11))
    pages_num = len(contents)
    cur_page = 1
    message = await msg.reply(embed=embed(f"{title}\n**Page {cur_page}/{pages_num}, {el_count} elements:**\n{' '.join(contents[cur_page-1])}"))
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == msg.author and str(reaction.emoji) in ["◀️", "▶️", '👍']
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await cli.wait_for("reaction_add", check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and cur_page != pages_num:
                cur_page += 1
                await message.edit(embed=embed(f"Page {cur_page}/{pages_num}, {el_count} elements:\n{' '.join(contents[cur_page-1])}"))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(embed=embed(f"Page {cur_page}/{pages_num}, {el_count} elements:\n{' '.join(contents[cur_page-1])}"))
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



class Admin:
    @staticmethod
    async def unregister(msg, roles, mongo):  # .unregister @mention
        if 'Admin' in roles or 'Staff' in roles:
            db = mongo['Season2']
            drivers_col = db['Drivers']
            cars_col = db['Cars']
            leagues_col = db['Leagues']

            for member in msg.mentions:
                driver = drivers_col.find_one({"id": member.id})
                car = cars_col.find_one({"id": driver['car']})
                cars_col.update_one({"id": driver['car']}, {"$inc": {"quantity": -1}})
                leagues_col.update_one({"id": driver['league']}, {"$inc": {"quantity": -1}})

                drivers_col.delete_one({"id": member.id})

                # reverts to Member
                member_role = get(msg.guild.roles, name='Member')
                driver_role = get(msg.guild.roles, name='Driver')
                league_role = get(msg.guild.roles, name=driver['league'])
                await member.remove_roles(driver_role)
                await member.add_roles(member_role)
                if league_role:
                    await member.remove_roles(league_role)

                car_role = get(msg.guild.roles, name=car['name'])
                await member.remove_roles(car_role)

                # removes number from nickname
                if member.nick is not None and member.nick.startswith('#'):
                    await member.edit(nick=member.nick.split(' ', 1)[1])
                await msg.reply(embed=embed(f'Unregistered {member.mention}'))

        else:
            await msg.reply(embed=embed('Insufficient permissions'))

    @staticmethod
    async def nickname(msg, roles):  # .nickname @mention nickname
        if 'Admin' in roles or 'Staff' in roles:
            member = msg.mentions[0]
            parameter = msg.content.split('>')[1].strip()

            if member.nick is None:
                await member.edit(nick=parameter)
            elif member.nick.startswith('#'):
                number = member.nick.split(' ', 1)[0].strip()
                await member.edit(nick=f'{number} {parameter}')
            else:
                await member.edit(nick=parameter)

            message = f"Edited nickname: {member.name}"
            message = embed(message)
            await msg.reply(embed=message)
        else:
            await msg.reply(embed=embed('Insufficient permissions'))

    @staticmethod
    async def role(msg, roles):  # .role @mention role, role
        if 'Admin' not in roles and 'Staff' not in roles:
            await msg.reply(embed=embed('Insufficient permissions'))
            return False
        member = msg.mentions[0]
        raw_parameters = msg.content.split('>')[1].split(',')
        parameters = list(map((lambda a: a.strip()), raw_parameters))
        message = f"Modified {member.name}: "
        roles = list(map((lambda a: a.name), msg.guild.roles))

        for param in parameters:
            findrole = find_re(roles, param)
            if 'Staff' in roles and (findrole == 'Admin' or findrole == 'Owner'):
                await msg.reply(embed=embed('NO'))
                return False
            if findrole:
                role_obj = get(msg.guild.roles, name=findrole)
                if get(member.roles, name=findrole) is None:
                    await member.add_roles(role_obj)
                    message += f" +{findrole}"
                else:
                    await member.remove_roles(role_obj)
                    message += f" -{findrole}"

        message = embed(message)
        await msg.reply(embed=message)

    @staticmethod
    async def addrole(msg, roles):  # .addrole role @mention, @mention
        if 'Admin' not in roles and 'Staff' not in roles:
            await msg.reply(embed=embed('Insufficient permissions'))
            return False
        role_str = ((msg.content.split(' ', 1)[1]).split('<')[0]).strip()
        roles = list(map((lambda a: a.name), msg.guild.roles))
        findrole = find_re(roles, role_str)
        if findrole:
            if 'Staff' in roles and (findrole == 'Admin' or findrole == 'Owner'):
                await msg.reply(embed=embed('NO'))
                return False
            role_obj = get(msg.guild.roles, name=findrole)
            message = ""

            for member in msg.mentions:
                if role_obj not in member.roles:
                    await member.add_roles(role_obj)
                    message += f"\nAdded role {findrole} to {member.name}"
                else:
                    message += f"\n{member.name} has NOT been modified - already has role {findrole}"

            message = embed(message)
            await msg.reply(embed=message)
        else:
            msg.reply(embed=embed('Role not found or found more than one matching'))

    @staticmethod
    async def removerole(msg, roles):  # .removerole role @mention, @mention
        if 'Admin' not in roles and 'Staff' not in roles:
            await msg.reply(embed=embed('Insufficient permissions'))
            return False
        role_str = ((msg.content.split(' ', 1)[1]).split('<')[0]).strip()
        roles = list(map((lambda a: a.name), msg.guild.roles))
        findrole = find_re(roles, role_str)
        if findrole:
            if 'Staff' in roles and (findrole == 'Admin' or findrole == 'Owner'):
                await msg.reply(embed=embed('NO'))
                return False
            role_obj = get(msg.guild.roles, name=findrole)
            message = ""

            for member in msg.mentions:
                if role_obj in member.roles:
                    await member.remove_roles(role_obj)
                    message += f"\nRemoved role {findrole} from {member.name}"
                else:
                    message += f"\n{member.name} has NOT been modified - did not have role {findrole}"

            message = embed(message)
            await msg.reply(embed=message)
        else:
            await msg.reply(embed=embed('Role not found or found more than one matching'))

    @staticmethod
    async def nuke(msg, roles):  # .nuke role
        if 'Admin' not in roles:
            await msg.reply(embed=embed('Insufficient permissions'))
            return False
        role_to_remove = msg.content.split(' ', 1)[1]
        role_obj = get(msg.guild.roles, name=role_to_remove)
        await msg.reply(embed=embed(f'Nuking {role_to_remove}...'))

        for member in msg.guild.members:
            await member.remove_roles(role_obj)

        await msg.reply(embed=embed(f'Nuked {role_to_remove}'))

    @staticmethod
    async def give_role_to_everyone(msg, roles):  # .nuke role
        if 'Admin' not in roles:
            await msg.reply(embed=embed('Insufficient permissions'))
            return False
        role_to_add = msg.content.split(' ')[1]
        role_obj = get(msg.guild.roles, name=role_to_add)
        await msg.reply(embed=embed(f'Giving everyone {role_to_add} role'))

        for member in msg.guild.members:
            await member.add_roles(role_obj)

        await msg.reply(embed=embed(f'Gave role {role_to_add} to everyone'))

    @staticmethod
    async def resetnicknames(msg, roles):  # .resetnicknames
        if 'Admin' in roles:
            member_role = get(msg.guild.roles, name='Member')

            for member in msg.guild.members:
                if member_role in member.roles:
                    try:
                        await member.edit(nick=None)
                    except Exception as ex:
                        pass

    @staticmethod
    async def resetnickname(msg, roles):  # .resetnickname @mentions
        if 'Admin' not in roles:
            await msg.reply(embed=embed('Insufficient permissions'))
            return False
        message = "Nickname reset: "
        for member in msg.mentions:
            await member.edit(nick=None)
            message += f"{member.name}, "

        message = embed(message)
        await msg.reply(embed=message)

    @staticmethod
    async def purge(msg, roles):  # .purge
        if 'Admin' in roles:
            if msg.content.startswith('.purge this channel please'):
                await msg.reply(embed=embed("Purging channel..."))
                await msg.channel.purge()
            else:
                await msg.reply(embed=embed("Say '.purge this channel please' to purge this channel"))
        else:
            await msg.reply("Don't you fucking dare")

    @staticmethod
    async def clear(cli, msg, roles):  # .clear [number]
        if 'Admin' in roles or 'Staff' in roles:
            number = int(msg.content.split(' ', 1)[1].strip()) + 1
            if number is None:
                await msg.reply(embed=embed('Provide a number of messages you would like to delete'))
            else:
                await msg.channel.purge(limit=number)
        # await embed_timeout(cli, msg, embed(f"Deleted {number - 1} message(s)"))

    @staticmethod
    async def lock(msg, roles):  # .lock or .cock
        if 'Admin' in roles:
            driver_role = get(msg.guild.roles, name='Driver')
            member_role = get(msg.guild.roles, name='Member')
            await msg.channel.set_permissions(driver_role, send_messages=False, view_channel=True)
            await msg.channel.set_permissions(member_role, send_messages=False, view_channel=True)
            await msg.reply(embed=embed('Channel has been locked'))

    @staticmethod
    async def unlock(msg, roles):  # .unlock or .uncock
        if 'Admin' in roles:
            driver_role = get(msg.guild.roles, name='Driver')
            member_role = get(msg.guild.roles, name='Member')
            await msg.channel.set_permissions(driver_role, send_messages=True, view_channel=True)
            await msg.channel.set_permissions(member_role, send_messages=True, view_channel=True)
            await msg.reply(embed=embed('Channel has been unlocked'))

    @staticmethod
    async def number(msg, roles, mongo):
        if 'Admin' in roles or 'Staff' in roles:
            number = msg.content.split('>')[1].strip()
            db = mongo['Season2']
            drivers_col = db['Drivers']

            if drivers_col.find_one({"nr": int(number)}):
                await msg.reply(embed=embed(f'Number {int(number)} is taken'))
                return False

            drivers_col.update_one({"id": msg.mentions[0].id}, {"$set": {"nr": int(number)}})
            await msg.mentions[0].edit(nick=f"#{number} {msg.mentions[0].nick.split(' ', 1)[1]}")
            await msg.reply(embed=embed(f"Number changed for {msg.mentions[0]} to {number}"))

    @staticmethod
    async def update_sheet(msg, roles, mongo):
        if 'Admin' in roles or 'Staff' in roles:
            db = mongo['Season2']
            drivers_col = db['Drivers']
            driver_role = get(msg.guild.roles, name='Driver')
            driverlist = []

            message = 'Sheet has been updated!'

            mongo_drivers = drivers_col.find({})
            for driver in mongo_drivers:
                dc_user = get(msg.guild.members, id=driver['id'])
                if dc_user is None:
                    drivers_col.delete_one({"id": driver['id']})
                    message += f"\nDeleted {driver['gt']}"
                else:
                    driverlist.append(driver)

            driverlist = list(map((lambda a: [a['nr'], a['gt'], a['dcname'], a['league'], a['car'], a['swaps']]), driverlist))
            update_gsheet(driverlist, mongo)

            await msg.reply(embed=embed(message))

    @staticmethod
    async def league(msg, roles, mongo):  # .league [league] [mentions]
        if 'Admin' in roles or 'Staff' in roles:
            league = msg.content.split(' ', 2)[1].strip().lower().capitalize()
            db = mongo['Season2']
            leagues_col = db['Leagues']
            drivers_col = db['Drivers']
            drivers = ""
            league_role = get(msg.guild.roles, name=league)

            for member in msg.mentions:
                driver_obj = drivers_col.find_one({"id": member.id})
                if driver_obj is not None:
                    if league.lower() == "placement":

                        league_to_remove = get(msg.guild.roles, name=driver_obj['league'])
                        await member.remove_roles(league_to_remove)
                        leagues_col.update_one({"id": driver_obj['league']}, {"$inc": {"quantity": -1}})
                        drivers_col.update_one({"id": member.id}, {"$set": {"league": "placement"}})

                    elif driver_obj['league'] == "placement":

                        drivers_col.update_one({"id": member.id}, {"$set": {"league": league}})
                        leagues_col.update_one({"id": league}, {"$inc": {"quantity": 1}})
                        await member.add_roles(league_role)

                    else:

                        leagues_col.update_one({"id": driver_obj['league']}, {"$inc": {"quantity": -1}})
                        leagues_col.update_one({"id": league}, {"$inc": {"quantity": 1}})
                        league_to_remove = get(msg.guild.roles, name=driver_obj['league'])
                        await member.remove_roles(league_to_remove)
                        await member.add_roles(league_role)
                        drivers_col.update_one({"id": member.id}, {"$set": {"league": league}})

                    drivers += f" {member.name}"

            await msg.reply(embed=embed(f'Assigned{drivers} to {league}'))

    @staticmethod
    async def edit(msg, mongo):
        params = msg.content.split('>')[1].split(',', 1)
        params = list(map(lambda a: a.strip(), params))

        if params[1].isdigit():
            params[1] = int(params[1])

        if params[0].strip() == "car":
            return False

        db = mongo['Season2']
        drivers_col = db['Drivers']

        drivers_col.update_one({"id": msg.mentions[0].id}, {"$set": {params[0]: params[1]}})
        await msg.reply(embed=embed(f"{params[0]} changed for {msg.mentions[0]} to {params[1]}"))

    @staticmethod
    async def patch_notes(msg, cli, roles, patch):
        if msg.author.name == 'Albannt' and 'Admin' in roles:
            params_ver = patch.split(' ', 1)
            version = params_ver[0]
            params = params_ver[1].split('/')
            today = date.today()

            message = dc.Embed(
                title=f'1Bot Patch Notes {today} - version {version}',
                color=15879747
            )
            for param in params:
                field = param.split(';')
                message.add_field(
                    name=field[0],
                    value=field[1],
                    inline=False
                )

            updatechannel = cli.get_channel(id=1029152874489454692)
            await updatechannel.send(embed=message)
            await msg.delete()
        else:
            return False


    @staticmethod
    async def testcommand(msg, mongo):
        db = mongo['Season2']
        drivers_col = db['Drivers']
        for member in msg.guild.members:
            if get(member.roles, name='Driver') and not get(member.roles, name='Admin'):
                driver = drivers_col.find_one({"id": member.id})
                await member.edit(nick=f"#{driver['nr']} {driver['gt']}")


    @staticmethod
    async def toyota_quali(msg): # not a command
        quali_role = get(msg.guild.roles, name='Ready Check')
        await msg.author.edit(nick=msg.content)
        await msg.author.add_roles(quali_role)


    @staticmethod
    async def toyota_list(msg, cli):
        quali_role = get(msg.guild.roles, name='Ready Check')
        quali_list = []
        for member in msg.guild.members:
            if quali_role in member.roles:
                quali_list.append(member.nick)

        await pages(cli, msg, quali_list, "Quali")





