from discord.utils import get
from json_util import json_read, json_write
from utils import embed, embed_timeout
from pprint import pprint
from gsheetio import update_sheet


class Admin:
    @staticmethod
    async def unregister(msg, roles, mongo):  # .unregister @mention
        if 'Admin' in roles or 'Staff' in roles:
            db = mongo['Season2']
            drivers_col = db['Drivers']
            cars_col = db['Cars']
            leagues_col = db['Leagues']

            driver = drivers_col.find_one()
            for member in msg.mentions:
                driver = drivers_col.find_one({"id": member.id})
                car = cars_col.find_one({"id": driver['car']})
                cars_col.update_one({"id": driver['car']}, {"$inc": {"quantity": -1}})
                leagues_col.update_one({"id": driver['league']}, {"$inc": {"quantity": -1}})

                drivers_col.delete_one({"id": member.id})

                # reverts to Member
                member_role = get(msg.guild.roles, name='Member')
                driver_role = get(msg.guild.roles, name='Driver')
                await member.remove_roles(driver_role)
                await member.add_roles(member_role)

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
        if 'Admin' in roles:
            member = msg.mentions[0]
            raw_parameters = msg.content.split('>')[1].split(',')
            parameters = list(map((lambda a: a.strip()), raw_parameters))
            message = f"Modified {member.name}: "

            for param in parameters:
                if get(member.roles, name=param) is None:
                    try:
                        role_obj = get(msg.guild.roles, name=param)
                        await member.add_roles(role_obj)
                        message += f" +{param}"
                    except AttributeError:
                        await msg.reply(f'Role {param} doesnt exist')
                else:
                    try:
                        role_obj = get(msg.guild.roles, name=param)
                        await msg.mentions[0].remove_roles(role_obj)
                        message += f" -{param}"
                    except AttributeError:
                        await msg.reply(f'Role {param} doesnt exist')

            message = embed(message)
            await msg.reply(embed=message)
        else:
            await msg.reply(embed=embed('Insufficient permissions'))

    @staticmethod
    async def addrole(msg, roles):  # .addrole role @mention, @mention
        if 'Admin' in roles:
            role_str = ((msg.content.split(' ', 1)[1]).split('<')[0]).strip()
            role_obj = get(msg.guild.roles, name=role_str)
            message = ""

            for member in msg.mentions:
                if role_obj not in member.roles:
                    await member.add_roles(role_obj)
                    message += f"\nAdded role {role_str} to {member.name}"
                else:
                    message += f"\n{member.name} has NOT been modified - already has role {role_str}"

            message = embed(message)
            await msg.reply(embed=message)
        else:
            await msg.reply(embed=embed('Insufficient permissions'))

    @staticmethod
    async def removerole(msg, roles):  # .removerole role @mention, @mention
        if 'Admin' in roles:
            role_str = ((msg.content.split(' ', 1)[1]).split('<')[0]).strip()
            role_obj = get(msg.guild.roles, name=role_str)
            message = ""

            for member in msg.mentions:
                if role_obj in member.roles:
                    await member.remove_roles(role_obj)
                    message += f"\nRemoved role {role_str} from {member.name}"
                else:
                    message += f"\n{member.name} has NOT been modified - doesn't have role {role_str}"

            message = embed(message)
            await msg.reply(embed=message)
        else:
            await msg.reply(embed=embed('Insufficient permissions'))

    @staticmethod
    async def nuke(msg, roles):  # .nuke role
        if 'Admin' in roles:
            role_to_remove = msg.content.split(' ', 1)[1]
            role_obj = get(msg.guild.roles, name=role_to_remove)
            await msg.reply(embed=embed(f'Nuking {role_to_remove}...'))

            for member in msg.guild.members:
                await member.remove_roles(role_obj)

            await msg.reply(embed=embed(f'Nuked {role_to_remove}'))

    @staticmethod
    async def give_role_to_everyone(msg, roles):  # .nuke role
        if 'Admin' in roles:
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
        if 'Admin' in roles:
            message = "Nickname reset: "
            for member in msg.mentions:
                await member.edit(nick=None)
                message += f"{member.name}, "

            message = embed(message)
            await msg.reply(embed=message)
        else:
            await msg.reply(embed=embed('Insufficient permissions'))

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
        if 'Admin' in roles:
            db = mongo['Season2']
            drivers_col = db['Drivers']
            cars_col = db['Cars']
            driver_role = get(msg.guild.roles, name='Driver')
            driverlist = []
            for member in msg.guild.members:
                if driver_role in member.roles:
                    driverlist.append(drivers_col.find_one({"id": member.id}, {'_id': 0, 'id': 0}))

            driverlist = list(map((lambda a: [a['nr'], a['gt'], a['dcname'], a['league'], a['car'], a['swaps']]), driverlist))
            pprint(driverlist)
            update_sheet(driverlist, mongo)
            await msg.reply(embed=embed('Sheet has been updated!'))

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




