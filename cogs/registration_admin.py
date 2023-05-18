import discord
from typing import Optional
from discord.ext import commands
from discord import app_commands
from pprint import pprint
from cogs.misc import utils
from cogs.misc.roles import Roles
from cogs.misc.divisions import Divisions
from cogs.misc.registration_checks import registration_check
from cogs.misc.connections import mongo
from discord.utils import get


role_ids = Roles()
div_laptimes = Divisions()


class RegistrationAdmin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('Registration_admin cog loaded')

    @commands.has_any_role(role_ids.staff, role_ids.admin, role_ids.owner)
    @commands.command()
    async def sync_registration_admin(self, ctx) -> None:
        try:
            synced = await ctx.bot.tree.sync(guild=discord.Object(id=1077859376414593124))
            await ctx.send(f"synced {len(synced)} RegistrationAdmin commands")
        except discord.HTTPException as er:
            await ctx.send(er)

    @app_commands.command(name='register_admin', description='Register someone for RH Endurance Championship[Admin]')
    @app_commands.checks.has_any_role(role_ids.staff, role_ids.admin, role_ids.owner)
    @app_commands.choices(car=[
        app_commands.Choice(name='Porsche', value='Porsche'),
        app_commands.Choice(name='Mercedes', value='Mercedes'),
        app_commands.Choice(name='Ferrari', value='Ferrari'),
        app_commands.Choice(name='Aston Martin', value='Aston Martin'),
        app_commands.Choice(name='Ford', value='Ford')
    ])
    @app_commands.describe(number='Between 2 and 999', gamertag='Your gamertag in Forza Horizon 5')
    async def register_admin(self, msg: discord.Interaction, number: app_commands.Range[int, 1, 999], gamertag: str, car: app_commands.Choice[str], target: discord.Member):
        db = mongo['RH']
        drivers_col = db['drivers']
        checks = await registration_check(number, gamertag, drivers_col, target.id)

        if not checks[0]:
            await msg.response.send_message(embed=utils.embed_failure(checks[1]))
            return

        driver = {
            "id": target.id,
            "gt": gamertag,
            "nr": number,
            "league": "placement",
            "placement": {
                "string": "",
                "ms": 0
            },
            "car": car.value,
            "swaps": 1,
            "dcname": target.name,
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

        member_role = get(msg.guild.roles, id=role_ids.member)
        driver_role = get(msg.guild.roles, id=role_ids.driver)
        car_role = get(msg.guild.roles, id=role_ids.cars[car.value])

        await target.remove_roles(member_role)
        await target.add_roles(driver_role)
        await target.add_roles(car_role)

        await target.edit(nick=f'#{number} {gamertag}')

        await msg.response.send_message(
            embed=utils.embed_success(f"Registered {target.name} with number #{number} and {car.name}")
        )


    @app_commands.command(name='swap_admin', description='Swap your car (only one swap avaliable!)[Admin]')
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff, role_ids.owner)
    @app_commands.choices(car=[
        app_commands.Choice(name='Porsche', value='Porsche'),
        app_commands.Choice(name='Mercedes', value='Mercedes'),
        app_commands.Choice(name='Ferrari', value='Ferrari'),
        app_commands.Choice(name='Aston Martin', value='Aston Martin'),
        app_commands.Choice(name='Ford', value='Ford')
    ])
    async def swap_admin(self, msg: discord.Interaction, car: app_commands.Choice[str], target: discord.Member):
        db = mongo['RH']
        drivers_col = db['drivers']

        driver = drivers_col.find_one({"id": target.id})

        if driver['swaps'] == 0:
            await msg.response.send_message(
                embed=utils.embed_failure(f"Swap not performed, {target.mention} doesn't have a swap avaliable")
            )
            return
        if driver['car'] == car.value:
            await msg.response.send_message(
                embed=utils.embed_failure(f"Swap not performed, {target.mention} already uses this car")
            )
            return

        role_to_del = get(msg.guild.roles, id=role_ids.cars[driver['car']])
        role_to_add = get(msg.guild.roles, id=role_ids.cars[car.value])

        await target.remove_roles(role_to_del)
        await target.add_roles(role_to_add)

        drivers_col.update_one({"id": target.id}, {"$set": {"car": car.value}})
        drivers_col.update_one({"id": target.id}, {"$inc": {"swaps": -1}})

        await msg.response.send_message(
            embed=utils.embed_success(f"Succesfully swapped to {car.name}!")
        )

    @app_commands.command(name='unregister', description='Unregister a driver[Admin]')
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff, role_ids.owner)
    async def unregister(self, msg: discord.Interaction, target: discord.Member):
        db = mongo['RH']
        drivers_col = db['drivers']

        driver = drivers_col.find_one({"id": target.id})

        if driver['league'] != 'placement':
            div_role_to_del = get(msg.guild.roles, id=role_ids.leagues[driver['league']])
            await target.remove_roles(div_role_to_del)

        car_role = get(msg.guild.roles, id=role_ids.cars[driver['car']])
        role_to_del = get(msg.guild.roles, id=role_ids.driver)
        role_to_add = get(msg.guild.roles, id=role_ids.member)

        await target.remove_roles(role_to_del, car_role)
        await target.add_roles(role_to_add)

        drivers_col.update({"id": target.id}, {'$set': {'nr': 0}})
        # drivers_col.delete_one({"id": target.id})

        if target.nick is not None and target.nick.startswith('#'):
            await target.edit(nick=target.nick.split(' ', 1)[1])

        await msg.response.send_message(embed=utils.embed_success(f"Unregistered {target.mention}"))


    @app_commands.command(name='number', description="Change a driver's number[Admin]")
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff, role_ids.owner)
    async def number(self, msg: discord.Interaction, target: discord.Member, number: app_commands.Range[int, 1, 999]):
        db = mongo['RH']
        drivers_col = db['drivers']

        if drivers_col.find_one({"nr": number}):
            await msg.response.send_message(embed=utils.embed_failure(f'Number {number} is taken'))
            return

        drivers_col.update_one({"id": target.id}, {"$set": {"nr": number}})
        await target.edit(nick=f"#{number} {target.nick.split(' ', 1)[1]}")
        await msg.response.send_message(embed=utils.embed_success(f"Number changed for {target.name} to {number}"))

    @app_commands.command(name='placement', description="[0:00.000 OR 00:00.000] USE THE EXACT FORMAT FROM THE SCREENSHOT[Admin]")
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff, role_ids.owner)
    async def placement(self, msg: discord.Interaction, target: discord.Member, laptime: str, finish_time: str):
        db = mongo['RH']
        drivers_col = db['drivers']


        laptime_ms = int(laptime[0]) * 60000 + int(laptime[2:4]) * 1000 + int(laptime[5:])


        if len(finish_time) == 8:
            finish_time_ms = int(finish_time[0]) * 60000 + int(finish_time[2:4]) * 1000 + int(finish_time[5:])
        else:
            finish_time_ms = int(finish_time[0:2]) * 60000 + int(finish_time[3:5]) * 1000 + int(finish_time[6:])
        div_name = div_laptimes.check_laptime(finish_time_ms)
        div_role = get(msg.guild.roles, id=role_ids.leagues[div_name])

        driver = drivers_col.find_one({"id": target.id})

        if driver:
            if driver['league'] != 'placement':
                role_to_remove = get(msg.guild.roles, id=role_ids.leagues[driver['league']])
                await target.remove_roles(role_to_remove)

            drivers_col.update_one({'id': target.id}, {"$set": {"placement": {
                "lap_string": laptime,
                "lap_ms": laptime_ms,
                "finish_string": finish_time,
                "finish_ms": finish_time_ms
            },
                "league": div_name
            }})
            await target.add_roles(div_role)

            await msg.response.send_message(embed=utils.embed_success(f"Set {target.name}'s times to {laptime}/{finish_time}, placed in {div_name} "))

            return

        await msg.response.send_message(embed=utils.embed_success(f"Driver not found in the database"))

    @commands.has_any_role(role_ids.staff, role_ids.admin, role_ids.owner)
    @commands.command()
    async def place_everyone(self, ctx) -> None:
        db = mongo['RH']
        drivers_col = db['drivers']

        mongo_drivers = drivers_col.find({})
        placed = 0

        for driver in mongo_drivers:
            dc_user = get(ctx.guild.members, id=driver['id'])
            if not dc_user:
                ctx.response.send_message(f"\n{driver['gt']} not found in the server, perform the /sync_driverlist command first")
                return

            div_name = div_laptimes.check_laptime(driver['placement']['finish_ms'])
            div_role = get(ctx.guild.roles, id=role_ids.leagues[div_name])

            if driver['placement']['finish_string'] == '':
                if get(ctx.guild.roles, id=role_ids.leagues['D1']) in dc_user.roles:
                    await dc_user.remove_roles(get(ctx.guild.roles, id=role_ids.leagues['D1']))
                if get(ctx.guild.roles, id=role_ids.leagues['D2']) in dc_user.roles:
                    await dc_user.remove_roles(get(ctx.guild.roles, id=role_ids.leagues['D2']))
                if get(ctx.guild.roles, id=role_ids.leagues['D3']) in dc_user.roles:
                    await dc_user.remove_roles(get(ctx.guild.roles, id=role_ids.leagues['D3']))

                if driver['league'] != 'placement':
                    role_to_remove = get(ctx.guild.roles, id=role_ids.leagues[driver['league']])
                    await dc_user.remove_roles(role_to_remove)
                    drivers_col.update_one({'id': driver['id']}, {"$set": {"league": 'placement'}})
                    await dc_user.add_roles(div_role)

            else:
                if driver['league'] != 'placement':
                    role_to_remove = get(ctx.guild.roles, id=role_ids.leagues[driver['league']])
                    await dc_user.remove_roles(role_to_remove)

                drivers_col.update_one({'id': driver['id']}, {"$set": {"league": div_name}})
                await dc_user.add_roles(div_role)

            placed += 1

        ctx.send(embed=utils.embed_success(f'Placed {placed} driver(s)'))

    @app_commands.command(name='gamertag', description="Change a driver's gamertag (doesn't change in sheets yet)[Admin]")
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff, role_ids.owner)
    async def gamertag(self, msg: discord.Interaction, target: discord.Member, gamertag: str):
        db = mongo['RH']
        drivers_col = db['drivers']

        await msg.response.send_message(f'Processing...')

        driver = drivers_col.find_one({'id': target.id})

        drivers_col.update_one({'id': target.id}, {"$set": {"gt": gamertag}})
        await target.edit(nick=f"#{driver['nr']} {gamertag}")

        await msg.edit_original_response(content='', embed=utils.embed_success(f'Gamertag updated for {target.mention}'))


async def setup(bot):
    await bot.add_cog(RegistrationAdmin(bot), guilds=[discord.Object(id=1077859376414593124)])



