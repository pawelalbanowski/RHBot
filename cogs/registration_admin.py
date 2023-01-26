import discord
from typing import Optional
from discord.ext import commands
from discord import app_commands
from pprint import pprint
from cogs.misc import utils
from cogs.misc.roles import Roles
from cogs.misc.registration_checks import registration_check
from cogs.misc.connections import mongo
from discord.utils import get


role_ids = Roles()


class RegistrationAdmin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('Registration_admin cog loaded')

    @app_commands.checks.has_any_role(role_ids.staff, role_ids.admin)
    @commands.command()
    async def sync_registration_admin(self, ctx) -> None:
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"synced {len(synced)} RegistrationAdmin commands")
        return

    @app_commands.command(name='register_admin', description='Register someone for 1HoR season 3[Admin]')
    @app_commands.checks.has_any_role(role_ids.staff, role_ids.admin)
    @app_commands.choices(car=[
        app_commands.Choice(name='Porsche', value='Porsche'),
        app_commands.Choice(name='Mercedes', value='Mercedes'),
        app_commands.Choice(name='Chevrolet', value='Chevrolet'),
        app_commands.Choice(name='Aston Martin', value='Aston Martin'),
        app_commands.Choice(name='Ford', value='Ford')
    ])
    @app_commands.describe(number='Between 2 and 999', gamertag='Your gamertag in Forza Horizon 5')
    async def register_admin(self, msg: discord.Interaction, number: app_commands.Range[int, 1, 999], gamertag: str, car: app_commands.Choice[str], target: discord.Member):
        db = mongo['Season3']
        drivers_col = db['Drivers']
        checks = await registration_check(number, gamertag, drivers_col, target.id)

        if not checks[0]:
            await msg.response.send_message(embed=utils.embed_failure(checks[1]))
            return

        driver = {
            "id": target.id,
            "gt": gamertag,
            "nr": number,
            "league": "placement",
            "placement": 0,
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
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff)
    @app_commands.choices(car=[
        app_commands.Choice(name='Porsche', value='Porsche'),
        app_commands.Choice(name='Mercedes', value='Mercedes'),
        app_commands.Choice(name='Chevrolet', value='Chevrolet'),
        app_commands.Choice(name='Aston Martin', value='Aston Martin'),
        app_commands.Choice(name='Ford', value='Ford')
    ])
    async def swap_admin(self, msg: discord.Interaction, car: app_commands.Choice[str], target: discord.Member):
        db = mongo['Season3']
        drivers_col = db['Drivers']

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
        drivers_col.update_one({"id": target.id}, {"$inc": {"swaps": 0}})

        await msg.response.send_message(
            embed=utils.embed_success(f"Succesfully swapped to {car.name}!")
        )

    @app_commands.command(name='unregister', description='Unregister a driver[Admin]')
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff)
    async def unregister(self, msg: discord.Interaction, target: discord.Member):
        db = mongo['Season3']
        drivers_col = db['Drivers']

        driver = drivers_col.find_one({"id": target.id})

        if driver['league'] != 'placement':
            div_role_to_del = get(msg.guild.roles, id=role_ids.leagues[driver['league']])
            await target.remove_roles(div_role_to_del)

        car_role = get(msg.guild.roles, id=role_ids.cars[driver['car']])
        role_to_del = get(msg.guild.roles, id=role_ids.driver)
        role_to_add = get(msg.guild.roles, id=role_ids.member)

        await target.remove_roles(role_to_del, car_role)
        await target.add_roles(role_to_add)

        drivers_col.delete_one({"id": target.id})

        if target.nick is not None and target.nick.startswith('#'):
            await target.edit(nick=target.nick.split(' ', 1)[1])

        await msg.response.send_message(embed=utils.embed_success(f"Unregistered {target.mention}"))


    @app_commands.command(name='number', description="Change a driver's number[Admin]")
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff)
    async def number(self, msg: discord.Interaction, target: discord.Member, number: app_commands.Range[int, 1, 999]):
        db = mongo['Season3']
        drivers_col = db['Drivers']

        if drivers_col.find_one({"nr": number}):
            await msg.response.send_message(embed=utils.embed_failure(f'Number {number} is taken'))
            return

        drivers_col.update_one({"id": target.id}, {"$set": {"nr": number}})
        await target.edit(nick=f"#{number} {target.nick.split(' ', 1)[1]}")
        await msg.response.send_message(embed=utils.embed_success(f"Number changed for {target.name} to {number}"))

async def setup(bot):
    await bot.add_cog(RegistrationAdmin(bot), guilds=[discord.Object(id=875740357055352833)])



