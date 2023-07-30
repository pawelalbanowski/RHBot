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
            if drivers_col.find_one({'nr': number}):
                await msg.edit_original_response(
                    content='',
                    embed=utils.embed_failure(
                        f"Number #{number} is taken")
                )
                return
            if checks[1].startswith('Gamertag') or checks[1].startswith('This'):
                driver = drivers_col.find_one({'id': msg.user.id})
                if driver and driver['nr'] == 0:

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

    @app_commands.checks.has_any_role(role_ids.member, role_ids.driver)
    @app_commands.command(name='event_participants', description='Get a list of drivers for an event')
    async def quali(self, msg: discord.Interaction):
        db = mongo['RH']
        drivers_col = db['drivers']

        gamertags = []

        await msg.response.send_message('Processing...')

        event_role = get(msg.guild.roles, id=role_ids.porsche_cup_ready)

        for member in msg.guild.members:
            if event_role in member.roles:
                driver = drivers_col.find_one({'id': member.id})
                if driver:
                    gamertags.append(f"#{driver['nr']} {driver['gt']} ({member.mention})")
        # embed = discord.Embed(
        #     title=f"List of drivers in event",
        #     color=15879747
        # )
        # embed.add_field(name="Drivers:", value='\n'.join(gamertags), inline=False)

        await msg.edit_original_response(content='\n'.join(gamertags))  # , embed=embed)

    @app_commands.command(name='offseason_streams', description="List streams for offseason event")
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff, role_ids.owner)
    async def offseason_streams(self, msg: discord.Interaction):
        db = mongo['RH']
        drivers_col = db['drivers']

        await msg.response.send_message('Processing...')

        streams = []

        driver_role = get(msg.guild.roles, id=role_ids.driver)
        split1_role = get(msg.guild.roles, id=role_ids.split1)

        for member in msg.guild.members:
            try:
                if driver_role in member.roles:
                    driver = drivers_col.find_one({'id': member.id})

                    if driver['stream'] and split1_role in member.roles:
                        streams.append(f"{driver['gt']} - {driver['stream']}")

            except Exception as er:
                pprint(er)
                await msg.channel.send_message(embed=utils.embed_failure(er))

        try:
            # embed = discord.Embed(
            #     title="Stream links:",
            #     color=15879747
            # )
            # embed.add_field(name=f"Streams", value='\n'.join(streams), inline=False)

        except Exception as er:
            pprint(er)
            await msg.channel.send_message(embed=utils.embed_failure(er))

        await msg.edit_original_response(content='\n'.join(streams))



async def setup(bot):
    await bot.add_cog(Offseason(bot), guilds=[discord.Object(id=1077859376414593124)])