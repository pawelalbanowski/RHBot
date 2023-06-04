from cogs.misc.connections import mongo


db = mongo['RH']
drivers_col = db['drivers']


driver = {
            "id": 435867024078536724,
            "gt": "ESV Justin",
            "nr": 0,
            "league": "placement",
            "placement": {
                "lap_string": "1:29.773",
                "lap_ms": 89773,
                "finish_string": "9:06.323",
                "finish_ms": 546323
            },
            "car": "Mercedes",
            "swaps": 1,
            "dcname": "Justintime",
            "results": {
                "r1": {
                    "quali": 0,
                    "race": 0,
                    "fl": 0
                },
                "r2": {
                    "quali": 0,
                    "race": 0,
                    "fl": 0
                },
                "r3": {
                    "quali": 0,
                    "race": 0,
                    "fl": 0
                },
                "r4": {
                    "quali": 0,
                    "race": 0,
                    "fl": 0
                },
                "r5": {
                    "quali": 0,
                    "race": 0,
                    "fl": 0
                },
                "r6": {
                    "quali": 0,
                    "race": 0,
                    "fl": 0
                },
                "r7": {
                    "quali": 0,
                    "race": 0,
                    "fl": 0
                },
            }
        }
drivers_col.insert_one(driver)