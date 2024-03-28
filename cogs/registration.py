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
        try:
            synced = await ctx.bot.tree.sync(guild=discord.Object(id=1077859376414593124))
            await ctx.send(f"synced {len(synced)} Registration commands")
        except discord.HTTPException as er:
            await ctx.send(er)

    @app_commands.command(name='register', description='Create your Racing Haven driver account')
    @app_commands.checks.has_role(role_ids.member)
    @app_commands.describe(gamertag='Your gamertag in Forza')
    async def register(self, msg: discord.Interaction, gamertag: str):
        db = mongo['RH']
        drivers_col = db['drivers']
        checks = await registration_check(gamertag, drivers_col, msg.user.id)

        if not checks[0]:
            await msg.response.send_message(embed=utils.embed_failure(checks[1]))
            return

        driver = {
            "id": msg.user.id,
            "gt": gamertag,
            "nr": 0,
            "dcname": msg.user.name,
            "stream": 0,
        }
        
        # "rhecs1": {
        #         "league": "placement",
        #         "placement": {
        #             "lap_string": "",
        #             "lap_ms": 100000,
        #             "finish_string": "",
        #             "finish_ms": 1000000
        #         },
        #         "car": car.value,
        #         "swaps": 1,
        #     },
        
        drivers_col.insert_one(driver)

        member_role = get(msg.guild.roles, id=role_ids.member)
        driver_role = get(msg.guild.roles, id=role_ids.driver)

        await msg.user.remove_roles(member_role)
        await msg.user.add_roles(driver_role)

        await msg.user.edit(nick=f'{gamertag}')

        await msg.response.send_message(
            embed=utils.embed_success(f"Registered {msg.user.name} as {gamertag}")
        )
        
    
    @app_commands.command(name='signup_rhec', description='Sign up for the Racing Haven Endurance Championship')
    @app_commands.checks.has_role(role_ids.driver)
    @app_commands.choices(car=[
        app_commands.Choice(name='Bentley', value='Bentley'),
        app_commands.Choice(name='Mercedes', value='Mercedes'),
        app_commands.Choice(name='Ferrari', value='Ferrari'),
        app_commands.Choice(name='McLaren', value='McLaren'),
        app_commands.Choice(name='BMW', value='BMW'),
        app_commands.Choice(name='Chevrolet', value='Chevrolet')
    ])
    def signup_rhec(self, msg: discord.Interaction, number: app_commands.Range[int, 1, 999], car: app_commands.Choice[str]):
        db = mongo['RH']
        drivers_col = db['drivers']

        driver = drivers_col.find_one({"id": msg.user.id})

        if driver['league'] != 'placement':
            return

        drivers_col.update_one({"id": msg.user.id}, {"$set": {"league": "rhec1"}})
        drivers_col.update_one({"id": msg.user.id}, {"$set": {"car": car.value}})

        role_to_del = get(msg.guild.roles, id=role_ids.leagues['placement'])
        role_to_add = get(msg.guild.roles, id=role_ids.leagues['rhec1'])
        role_to_car = get(msg.guild.roles, id=role_ids.cars[car.value])

        msg.user.remove_roles(role_to_del)
        msg.user.add_roles(role_to_add)
        msg.user.add_roles(role_to_car)

        msg.response.send_message(
            embed=utils.embed_success(f"Signed up for RHEC with number {number} and {car}!")
        )


    @app_commands.command(name='swap', description='Swap your car (only one swap avaliable!)')
    @app_commands.checks.has_role(role_ids.driver)
    @app_commands.choices(car=[
        app_commands.Choice(name='Bentley', value='Bentley'),
        app_commands.Choice(name='Mercedes', value='Mercedes'),
        app_commands.Choice(name='Ferrari', value='Ferrari'),
        app_commands.Choice(name='McLaren', value='McLaren'),
        app_commands.Choice(name='BMW', value='BMW'),
        app_commands.Choice(name='Chevrolet', value='Chevrolet')
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
        if driver['league'] != 'placement':
            drivers_col.update_one({"id": msg.user.id}, {"$inc": {"swaps": -1}})

        await msg.response.send_message(
            embed=utils.embed_success(f"Succesfully swapped to {car.name}!")
        )

    @app_commands.command(name='stream_link', description='Update your stream link (Twitch, YouTube)')
    @app_commands.describe(link='Enter the full link (for example https://twitch.tv/racinghaven)')
    @app_commands.checks.has_role(role_ids.driver)
    async def stream_link(self, msg: discord.Interaction, link: str):
        db = mongo['RH']
        drivers_col = db['drivers']

        await msg.response.send_message(f'Processing...')

        drivers_col.update_one({'id': msg.user.id}, {"$set": {"stream": link}})

        await msg.edit_original_response(content='',
                                         embed=utils.embed_success(f'Stream link updated for {msg.user.mention}: {link}'))


async def setup(bot):
    await bot.add_cog(Registration(bot), guilds=[discord.Object(id=1077859376414593124)])



