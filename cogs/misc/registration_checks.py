from pprint import pprint


async def registration_check(nr, gt, drivers_col, dc_id):
    try:
        if nr not in list(range(1, 1000)):
            return [False, "Number needs to be between 1-999"]
        if drivers_col.find_one({"nr": nr}):
            return [False, f'Number {nr} is taken']
        if drivers_col.find_one({"gt": gt}):
            return [False, f'Gamertag {gt} is taken']
        if drivers_col.find_one({"id": dc_id}):
            return [False, 'This Discord account is already registered']

        return [True]

    except Exception as er:
        return [False, er]


