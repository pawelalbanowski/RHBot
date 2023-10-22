from cogs.misc.connections import mongo
from pprint import pprint


db = mongo['lq']
test_col = db['regs_weekly']


# reserved = get()

res = test_col.find_one({'active': True})

pprint(res)