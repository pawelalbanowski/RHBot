import discord
from discord.ext import commands
from discord import app_commands
from pprint import pprint
from cogs.misc import utils
from cogs.misc.roles import Roles
from cogs.misc.registration_checks import registration_check
from cogs.misc.connections import mongo
from discord.utils import get


role_ids = Roles()


class Registration(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('Registration cog loaded')

    @commands.has_any_role(role_ids.staff, role_ids.admin, role_ids.owner)
    @commands.command()
    async def sync_registration(self, ctx) -> None:
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"synced {len(synced)} Registration commands")
        return

    @app_commands.command(name='register', description='Register yourself for RH Endurance Championship')
    @app_commands.checks.has_role(role_ids.member)
    @app_commands.choices(car=[
        app_commands.Choice(name='Porsche', value='Porsche'),
        app_commands.Choice(name='Mercedes', value='Mercedes'),
        app_commands.Choice(name='Ferrari', value='Ferrari'),
        app_commands.Choice(name='Aston Martin', value='Aston Martin'),
        app_commands.Choice(name='Ford', value='Ford')
    ])
    @app_commands.describe(number='Between 2 and 999', gamertag='Your gamertag in Forza Horizon 5')
    async def register(self, msg: discord.Interaction, number: app_commands.Range[int, 2, 999], gamertag: str, car: app_commands.Choice[str]):
        db = mongo['RH']
        drivers_col = db['drivers']
        checks = await registration_check(number, gamertag, drivers_col, msg.user.id)

        if not checks[0]:
            await msg.response.send_message(embed=utils.embed_failure(checks[1]))
            return

        driver = {
            "id": msg.user.id,
            "gt": gamertag,
            "nr": number,
            "league": "placement",
            "placement": {
                "string": "",
                "ms": 100000
            },
            "car": car.value,
            "swaps": 1,
            "dcname": msg.user.name,
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

        await msg.user.remove_roles(member_role)
        await msg.user.add_roles(driver_role)
        await msg.user.add_roles(car_role)

        await msg.user.edit(nick=f'#{number} {gamertag}')

        await msg.response.send_message(
            embed=utils.embed_success(f"Registered {msg.user.name} with number #{number} and {car.name}")
        )


    @app_commands.command(name='swap', description='Swap your car (only one swap avaliable!)')
    @app_commands.checks.has_role(role_ids.driver)
    @app_commands.choices(car=[
        app_commands.Choice(name='Porsche', value='Porsche'),
        app_commands.Choice(name='Mercedes', value='Mercedes'),
        app_commands.Choice(name='Ferrari', value='Ferrari'),
        app_commands.Choice(name='Aston Martin', value='Aston Martin'),
        app_commands.Choice(name='Ford', value='Ford')
    ])
    async def swap(self, msg: discord.Interaction, car: app_commands.Choice[str]):
        db = mongo['RH']
        drivers_col = db['drivers']

        driver = drivers_col.find_one({"id": msg.user.id})

        if driver['swaps'] == 0:
            await msg.response.send_message(
                embed=utils.embed_failure(f"Swap not performed, {msg.user.mention} doesn't have a swap avaliable")
            )
            return
        if driver['car'] == car.value:
            await msg.response.send_message(
                embed=utils.embed_failure(f"Swap not performed, {msg.user.mention} already uses this car")
            )
            return

        role_to_del = get(msg.guild.roles, id=role_ids.cars[driver['car']])
        role_to_add = get(msg.guild.roles, id=role_ids.cars[car.value])

        await msg.user.remove_roles(role_to_del)
        await msg.user.add_roles(role_to_add)

        drivers_col.update_one({"id": msg.user.id}, {"$set": {"car": car.value}})
        # drivers_col.update_one({"id": msg.user.id}, {"$inc": {"swaps": -1}})

        await msg.response.send_message(
            embed=utils.embed_success(f"Succesfully swapped to {car.name}!")
        )


async def setup(bot):
    await bot.add_cog(Registration(bot), guilds=[discord.Object(id=1077859376414593124)])



