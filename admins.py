from discord.utils import get
from json_util import json_read, json_write
from utils import embed, embed_timeout
from pprint import pprint


class Admin:
    @staticmethod
    async def unregister(msg, roles):  # .unregister @mention
        if 'Admin' in roles:
            reg_data = json_read("drivers.json")
            for member in msg.mentions:
                chosen_car = "0"

                for driver in reg_data["drivers"]:
                    if driver["id"] == member.id:
                        chosen_car = driver["car"]
                        reg_data["drivers"].remove(driver)

                for car in reg_data["cars"]:
                    if car["id"] == chosen_car:
                        car["quantity"] -= 1

                # reverts to Member
                member_role = get(msg.guild.roles, name='Member')
                driver_role = get(msg.guild.roles, name='Driver')
                await member.remove_roles(driver_role)
                await member.add_roles(member_role)

                # removes number from nickname
                if member.nick is not None and member.nick.startswith('#'):
                    await member.edit(nick=member.nick[4:])
                await msg.reply(embed=embed(f'Unregistered {member.mention}'))

            json_write("drivers.json", reg_data)
        else:
            await msg.reply(embed=embed('Insufficient permissions'))

    @staticmethod
    async def nickname(msg, roles):  # .nickname @mention nickname
        if 'Admin' in roles:
            member = msg.mentions[0]
            parameter = msg.content.split('>')[1].strip()

            if member.nick is None:
                await member.edit(nick=parameter)
            elif member.nick.startswith('#'):
                await member.edit(nick=f'{member.nick[0:4]}{parameter}')
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
    async def clear(cli, msg):  # .clear [number]
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
    async def testcommand(msg, roles, mongo):
        if 'Admin' in roles:
            msg.reply(mongo.list_database_names())
            pprint(mongo.list_database_names())
