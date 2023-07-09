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


class Offseason(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('Offseason cog loaded')

    @commands.has_any_role(role_ids.staff, role_ids.admin, role_ids.owner)
    @commands.command()
    async def sync_offseason(self, ctx) -> None:
        try:
            synced = await ctx.bot.tree.sync(guild=discord.Object(id=1077859376414593124))
            await ctx.send(f"synced {len(synced)} Offseason commands")
        except discord.HTTPException as er:
            await ctx.send(er)

    @app_commands.command(name='register_offseason', description='Register yourself for RH Offseason')
    @app_commands.checks.has_role(role_ids.member)
    @app_commands.describe(number='Between 2 and 999', gamertag='Your gamertag in Forza Horizon 5')
    async def register_offseason(self, msg: discord.Interaction, number: app_commands.Range[int, 2, 999], gamertag: str):
        db = mongo['RH']
        drivers_col = db['drivers']

        await msg.response.send_message(f'Processing...')

        checks = await registration_check(number, gamertag, drivers_col, msg.user.id)

        if len(checks) == 2:
            if checks[1].startswith('Gamertag'):
                driver = drivers_col.find_one({'id': msg.user.id})
                if driver and driver['nr'] == 0:
                    if drivers_col.find_one({'nr': number}):
                        await msg.response.send_message(
                            embed=utils.embed_failure(f"Number #{number} is taken")
                        )
                        return

                    drivers_col.update_one({'id': msg.user.id}, {'$set': {'nr': number}})

                    driver_role = get(msg.guild.roles, id=role_ids.driver)
                    member_role = get(msg.guild.roles, id=role_ids.member)

                    await msg.user.add_roles(driver_role)
                    await msg.user.remove_roles(member_role)

                    await msg.user.edit(nick=f"#{number} {driver['gt']}")

                    await msg.edit_original_response(
                        content='',
                        embed=utils.embed_success(f"Registered returning driver {msg.user.name} with number #{number}")
                    )


        if not checks[0]:
            await msg.response.send_message(embed=utils.embed_failure(checks[1]))
            return

        driver = {
            "id": msg.user.id,
            "gt": gamertag,
            "nr": number,
            "dcname": msg.user.name,
            "reserved_num": 0
            }

        drivers_col.insert_one(driver)

        member_role = get(msg.guild.roles, id=role_ids.member)
        driver_role = get(msg.guild.roles, id=role_ids.driver)

        await msg.user.remove_roles(member_role)
        await msg.user.add_roles(driver_role)

        await msg.user.edit(nick=f'#{number} {gamertag}')

        await msg.edit_original_response(
            content='',
            embed=utils.embed_success(f"Registered {msg.user.name} with number #{number}")
        )



async def setup(bot):
    await bot.add_cog(Offseason(bot), guilds=[discord.Object(id=1077859376414593124)])