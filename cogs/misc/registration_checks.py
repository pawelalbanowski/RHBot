from pprint import pprint


async def registration_check(gt, drivers_col, dc_id):
    try:
        if drivers_col.find_one({"gt": gt}):
            return [False, f'Gamertag {gt} is already registered']
        if drivers_col.find_one({"id": dc_id}):
            return [False, 'This Discord account is already registered']

        return [True]

    except Exception as er:
        return [False, er]


