from pprint import pprint
import gspread


async def registration_check(msg, parameters, reg_data, dcid):
    if parameters[0].isdigit() and int(parameters[0]) in list(range(1, 99)) \
            and len(parameters[0]) == 2 and int(parameters[2]) in list(range(1, 6)):
        try:
            for driver in reg_data['drivers']:
                if parameters[0] == driver['nr']:
                    msg.reply(f'Number {parameters[0]} is taken')
                    return False
                if parameters[1] == driver['gt']:
                    msg.reply(f'Gamertag {parameters[1]} is already registered')
                    return False
                if dcid == driver['id']:
                    msg.reply(f'That Discord account is already registered')
                    return False
            for car in reg_data["cars"]:
                if car["id"] == parameters[2]:
                    if car["quantity"] >= 15:
                        msg.reply(f'Maximum number of drivers for {car["name"]} has been reached')
                        return False
            return True
        except Exception as exc:
            pprint(exc)
    else:
        await msg.reply('Invalid argument(s)')







# async def registration_check(msg, parameters):
#     if parameters[0].isdigit() and len(parameters[0]) == 2:
#         try:
#             gc = gspread.service_account()
#             sheet = gc.open('1HoR bot data test')
#             id_check = sheet.sheet1.find(str(msg.author.id))
#             gt_check = sheet.sheet1.find(parameters[1])
#             number_check = sheet.sheet1.find(parameters[0])
#             if id_check is None and gt_check is None:
#                 if number_check is None:
#                     pprint('number check success')
#                     return True
#                 else:
#                     await msg.reply('Number already taken')
#                     return False
#             else:
#                 await msg.reply('Duplicate submission, you already registered')
#                 return False
#         except AttributeError as exc:
#             pprint(exc)
#     else:
#         await msg.reply('Invalid arguments')
