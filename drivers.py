from checks import registration_check
from discord.utils import get
from json_util import json_read, json_write
from utils import embed
from pprint import pprint


class Driver:
    @staticmethod
    async def register(msg, roles, mongo):  # .register nr, gt, car or .register @mention nr, gt, car
        # admin registering other user
        if len(msg.mentions) != 0:
            if 'Admin' in roles:
                member = msg.mentions[0]
                raw_parameters = msg.content.split('>')[1].split(',')
                parameters = list(map((lambda a: a.strip()), raw_parameters))
                db = mongo['Season2']
                drivers_col = db['Drivers']
                cars_col = db['Cars']
                check = await registration_check(msg, parameters, drivers_col, cars_col, msg.author.id)
                if check:
                    # add driver to json
                    driver = {
                        "id": msg.mentions[0].id,
                        "gt": parameters[1],
                        "nr": parameters[0],
                        "league": "placement",
                        "car": (parameters[2]).lower().capitalize(),
                        "swaps": 0
                    }
                    drivers_col.insert_one(driver)

                    # modify roles
                    member_role = get(msg.guild.roles, name='Member')
                    driver_role = get(msg.guild.roles, name='Driver')
                    await member.remove_roles(member_role)
                    await member.add_roles(driver_role)

                    car = (cars_col.find_one({"id": (parameters[2]).lower().capitalize()}))['name']
                    car_role = get(msg.guild.roles, name=car)
                    await member.add_roles(car_role)

                    # edit nickname
                    if msg.mentions[0].nick is None:
                        await msg.mentions[0].edit(nick=f'#{parameters[0]} {member.name}')
                    else:
                        await msg.mentions[0].edit(nick=f'#{parameters[0]} {member.nick}')
                    await msg.reply(embed=embed(f'Registered {member.mention} with number {parameters[0]} and {(parameters[2]).lower().capitalize()}'))
            else:
                await msg.reply(embed=embed('Insufficient permissions'))
                return False
        # user registering themselves
        elif 'Member' in roles:
            raw_parameters = (msg.content.split(' ', 1)[1]).split(',')
            parameters = list(map((lambda a: a.strip()), raw_parameters))
            db = mongo['Season2']
            drivers_col = db['Drivers']
            cars_col = db['Cars']
            check = await registration_check(msg, parameters, drivers_col, cars_col, msg.author.id)
            if check:
                # add driver to json
                driver = {
                    "id": msg.author.id,
                    "gt": parameters[1],
                    "nr": int(parameters[0]),
                    "league": "placement",
                    "car": (parameters[2]).lower().capitalize(),
                    "swaps": 0
                }
                drivers_col.insert_one(driver)

                # modify roles
                member_role = get(msg.guild.roles, name='Member')
                driver_role = get(msg.guild.roles, name='Driver')
                await msg.author.remove_roles(member_role)
                await msg.author.add_roles(driver_role)

                car = (cars_col.find_one({"id": (parameters[2]).lower().capitalize()}))['name']
                car_role = get(msg.guild.roles, name=car)
                await msg.author.add_roles(car_role)

                # edit nickname
                if msg.author.nick is None:
                    await msg.author.edit(nick=f'#{parameters[0]} {msg.author.name}')
                else:
                    await msg.author.edit(nick=f'#{parameters[0]} {msg.author.nick}')
                await msg.reply(embed=embed(f'Registered {msg.author.name} with number #{parameters[0]} and {(parameters[2]).lower().capitalize()}'))
        else:
            await msg.reply(embed=embed('Already registered'))
            return False

    @staticmethod
    async def swap(msg, roles, mongo):  # .swap car or .swap car @mention
        if len(msg.mentions) != 0:
            if 'Admin' in roles:
                member = msg.mentions[0]
                raw_parameters = msg.content.split('>')[1].split(',')
                parameters = list(map((lambda a: a.strip()), raw_parameters))
                db = mongo['Season2']
                drivers_col = db['Drivers']
                cars_col = db['Cars']
                chosen_car = parameters[0].lower().capitalize()

                driver = drivers_col.find_one({"id": member.id})
                if driver['car'] == chosen_car:
                    msg.reply(embed=embed(f"Swap not performed, {member.mention} already uses this car"))
                    return
                if cars_col.find_one({"id": chosen_car}) is None:
                    msg.reply(embed=embed("Invalid car alias"))
                    return
                
                role_to_del = (cars_col.find_one({"id": driver['car']}))['name']
                role_to_add = (cars_col.find_one({"id": chosen_car}))['name']
                
                role_obj1 = get(msg.guild.roles, name=role_to_del)
                await member.remove_roles(role_obj1)
                
                role_obj2 = get(msg.guild.roles, name=role_to_add)
                await member.add_roles(role_obj2)
                
                cars_col.update_one({"id": driver['car']}, {"$inc": {"quantity": 1}})
                drivers_col.update_one({"id": member.id}, {"$set": {"car": chosen_car}})
                cars_col.update_one({"id": chosen_car}, {"$inc": {"quantity": 1}})
                
                
                
                await msg.reply(embed=embed("Car swap successful!"))
                return
        else:
            if 'Driver' in roles:
                # need to refactor
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


