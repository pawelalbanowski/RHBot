from checks import registration_check
from discord.utils import get
from json_util import json_read, json_write
from utils import embed, pages
from pprint import pprint


async def register(msg, roles):  # .register nr, gt, car or .register @mention nr, gt, car
    # admin registering other user
    if len(msg.mentions) != 0:
        if 'Admin' in roles:
            member = msg.mentions[0]
            raw_parameters = msg.content.split('>')[1].split(',')
            parameters = list(map((lambda a: a.strip()), raw_parameters))
            reg_data = json_read("drivers.json")
            check = await registration_check(msg, parameters, reg_data, member.id)
            if check:
                # add driver to json
                driver = {
                    "id": msg.mentions[0].id,
                    "gt": parameters[1],
                    "nr": parameters[0],
                    "league": 0,
                    "car": parameters[2],
                    "swaps": 0
                }
                reg_data["drivers"].append(driver)
                
                # increase total on the chosen car
                for car in reg_data["cars"]:
                    if car["id"] == parameters[2]:
                        car["quantity"] += 1
                        chosen_car = car["name"]
                        
                json_write("drivers.json", reg_data)
                
                # modify roles
                member_role = get(msg.guild.roles, name='Member')
                driver_role = get(msg.guild.roles, name='Driver')
                await member.remove_roles(member_role)
                await member.add_roles(driver_role)
                
                # edit nickname
                if msg.mentions[0].nick is None:
                    await msg.mentions[0].edit(nick=f'#{parameters[0]} {member.name}')
                else:
                    await msg.mentions[0].edit(nick=f'#{parameters[0]} {member.nick}')
                await msg.reply(embed=embed(f'Registered {member.mention} with number {parameters[0]} and {chosen_car}'))
        else:
            await msg.reply(embed=embed('Insufficient permissions'))
            return False
    # user registering themselves
    elif 'Member' in roles:
        raw_parameters = (msg.content.split(' ', 1)[1]).split(',')
        parameters = list(map((lambda a: a.strip()), raw_parameters))
        reg_data = json_read("drivers.json")
        check = await registration_check(msg, parameters, reg_data, msg.author.id)
        if check:
            # add driver to json
            driver = {
                "id": msg.author.id,
                "gt": parameters[1],
                "nr": int(parameters[0]),
                "league": 0,
                "car": parameters[2],
                "swaps": 0
            }
            reg_data["drivers"].append(driver)
            
            # increase total on the chosen car
            for car in reg_data["cars"]:
                if car["id"] == parameters[2]:
                    car["quantity"] += 1
                    chosen_car = car["name"]
                    
            json_write("drivers.json", reg_data)
            
            # modify roles
            member_role = get(msg.guild.roles, name='Member')
            driver_role = get(msg.guild.roles, name='Driver')
            await msg.author.remove_roles(member_role)
            await msg.author.add_roles(driver_role)
            
            # edit nickname
            if msg.author.nick is None:
                await msg.author.edit(nick=f'#{parameters[0]} {msg.author.name}')
            else:
                await msg.author.edit(nick=f'#{parameters[0]} {msg.author.nick}')
            await msg.reply(embed=embed(f'Registered {msg.author.mention} with number #{parameters[0]} and {chosen_car}'))
    else:
        await msg.reply(embed=embed('Already registered'))
        return False


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


async def swap(msg, roles):  # .swap car or .swap car @mention
    if len(msg.mentions) != 0:
        if 'Admin' in roles:
            member = msg.mentions[0]
            raw_parameters = msg.content.split('>')[1].split(',')
            parameters = list(map((lambda a: a.strip()), raw_parameters))
            reg_data = json_read("drivers.json")
            
            for driver in reg_data['drivers']:
                if driver["id"] == member.id:
                    for car in reg_data["cars"]:
                        if car["id"] == parameters[0]:
                            car["quantity"] += 1
                        if car["id"] == driver["car"]:
                            car["quantity"] -= 1
                            
                    driver["car"] = parameters[0]
                    await msg.reply(embed=embed("Car swap successful!"))
                    json_write("drivers.json", reg_data)
                    return
    else:
        if 'Driver' in roles:
            parameter = (msg.content.split(' ', 1)[1]).strip()
            reg_data = json_read("drivers.json")
            
            if int(parameter) in list(range(1, 6)):
                for driver in reg_data['drivers']:
                    if driver["id"] == msg.author.id:
                        if driver["swaps"] == 0:
                            
                            for car in reg_data["cars"]:
                                if car["id"] == parameter:
                                    car["quantity"] += 1
                                if car["id"] == driver["car"]:
                                    car["quantity"] -= 1
                                    
                            driver["car"] = parameter
                            driver["swaps"] = 1
                            await msg.reply(f"Car swap successful!")
                            json_write("drivers.json", reg_data)
                        else:
                            await msg.reply(embed=embed("Car swap already used"))
            else:
                await msg.reply(embed=embed('Invalid car id'))


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


async def addrole(msg, roles):  # .addrole role, @mention, @mention
    if 'Admin' in roles:
        role_str = (msg.content.split(' ', 1)[1]).split(',')[0]
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


async def removerole(msg, roles):  # .removerole role, @mention, @mention
    if 'Admin' in roles:
        role_str = (msg.content.split(' ', 1)[1]).split(',')[0]
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


async def nuke(msg, roles):  # .nuke role
    if 'Admin' in roles:
        role_to_remove = msg.content.split(' ', 1)[1]
        role_obj = get(msg.guild.roles, name=role_to_remove)
        await msg.reply(embed=embed(f'Nuking {role_to_remove}...'))

        for member in msg.guild.members:
            await member.remove_roles(role_obj)
           
        await msg.reply(embed=embed(f'Nuked {role_to_remove}'))


async def give_role_to_everyone(msg, roles):  # .nuke role
    if 'Admin' in roles:
        role_to_add = msg.content.split(' ')[1]
        role_obj = get(msg.guild.roles, name=role_to_add)
        await msg.reply(embed=embed(f'Giving everyone {role_to_add} role'))
        
        for member in msg.guild.members:
            await member.add_roles(role_obj)
            
        await msg.reply(embed=embed(f'Gave role {role_to_add} to everyone'))


async def resetnicknames(msg, roles):  # .resetnicknames
    if 'Admin' in roles:
        member_role = get(msg.guild.roles, name='Member')
        
        for member in msg.guild.members:
            if member_role in member.roles:
                try:
                    await member.edit(nick=None)
                except Exception as ex:
                    pass


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


async def clear(msg):  # .clear [number]
    number = int(msg.content.split(' ', 1)[1].strip()) + 1
    await msg.channel.purge(limit=number)
    await msg.channel.send(embed=embed(f"Deleted {number - 1} message(s)"))


async def purge(msg, roles):  # .purge
    if 'Admin' in roles:
        if msg.content.startswith('.purge this channel please'):
            await msg.reply("Purging channel...")
            await msg.channel.purge()
        else:
            await msg.reply("Say '.purge this channel please' to purge this channel")
    else:
        await msg.reply("Don't you fucking dare")


async def pet(msg):  # .pet
    await msg.reply(f'Fuck you {msg.author.mention}')


async def gnfos(msg):  # .gnfos
    await msg.reply('Good neighbors from our server :pray:')


async def fh5(msg):  # .fh5
    await msg.reply('Forza Horizon 5 is a perfect game with no obvious flaws!')


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

