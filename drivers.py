from checks import registration_check
from discord.utils import get
from json_util import json_read, json_write
from utils import embed
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


