from pprint import pprint
import gspread
from utils import embed


async def registration_check(msg, parameters, drivers_col, cars_col, dcid):
    if parameters[0].isdigit() and int(parameters[0]) in list(range(1, 1000)):
        try:
            if drivers_col.find_one({"nr": int(parameters[0])}):
                await msg.reply(embed=embed(f'Number {int(parameters[0])} is taken'))
                return False
            # check for gamertag
            if drivers_col.find_one({"gt": parameters[1]}):
                await msg.reply(embed=embed(f'Gamertag {parameters[1]} is already registered'))
                return False
            # check for dc account
            if drivers_col.find_one({"id": dcid}):
                await msg.reply(embed=embed(f'That Discord account is already registered'))
                return False
            
            # check for car avaliability
            car = cars_col.find_one({"id": (parameters[2]).lower().capitalize()})
            if car:
                cars_col.update_one({"id": (parameters[2]).lower().capitalize()}, {"$inc": {"quantity": 1}})
            else:
                await msg.reply(embed=embed(f"Car {(parameters[2]).lower().capitalize()} doesn't exist. Try again"))
                return False

            return True
        except Exception as exc:
            pprint(exc)
    else:
        await msg.reply(embed=embed("Invalid number, make sure it's between 1 and 999"))
