import discord
from typing import Optional
from discord.ext import commands
from discord import app_commands
from pprint import pprint
from cogs.misc import utils
from cogs.misc.roles import Roles
from cogs.misc.connections import mongo
from discord.utils import get
from cogs.misc.gsheetio import update_gsheet


role_ids = Roles()


class Administration(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('Administration cog loaded')

    @commands.has_any_role(role_ids.staff, role_ids.admin, role_ids.owner)
    @commands.command()
    async def sync_administration(self, ctx) -> None:
        try:
            synced = await ctx.bot.tree.sync(guild=discord.Object(id=1077859376414593124))
            await ctx.send(f"synced {len(synced)} Administration commands")
        except discord.HTTPException as er:
            await ctx.send(er)

    @commands.has_role(role_ids.owner)
    @commands.command()
    async def test_command(self, ctx) -> None:
        db = mongo['RH']
        drivers_col = db['drivers']

        drivers_col.update_many({}, {"$set": {"placement": {
            "lap_string": "",
            "lap_ms": 100000,
            "finish_string": "",
            "finish_ms": 1000000
        }}})
        await ctx.send("fuck you")


    @app_commands.command(name='sync_driverlist', description='Update driver master sheet[Admin]')
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff, role_ids.owner)
    async def sync_driverlist(self, msg: discord.Interaction):
        db = mongo['RH']
        drivers_col = db['drivers']

        driverlist = []

        await msg.response.send_message(f'Processing...')

        message = 'Sheet has been updated!'
        mongo_drivers = drivers_col.find({})
        for driver in mongo_drivers:
            dc_user = get(msg.guild.members, id=driver['id'])
            if not dc_user:
                drivers_col.delete_one({'id': driver['id']})
                message += f"\nDeleted {driver['gt']}"
            else:
                driverlist.append(driver)

        sorted_placement = sorted(driverlist, key=lambda d: d['placement']['finish_ms'])

        driverlist = list(map((
                lambda a: [a['nr'], a['gt'], a['dcname'], a['league'], a['car'], a['swaps'], a['placement']['lap_string'], a['placement']['finish_string']]
             ), driverlist))

        sorted_placement = list(map((
                lambda a: [a['nr'], a['gt'], a['dcname'], a['league'], a['car'], a['swaps'], a['placement']['lap_string'], a['placement']['finish_string']]
             ), sorted_placement))

        update_gsheet(driverlist, mongo, 0)
        update_gsheet(sorted_placement, mongo, 1)


        await msg.edit_original_response(content='', embed=utils.embed_success(message))


    @app_commands.command(name='clear', description='clear [number] of messages')
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff, role_ids.owner)
    async def clear(self, msg: discord.Interaction, number: int):
        await msg.response.send_message(embed=utils.embed_success(f'Deleted {number} message(s)'), ephemeral=True)
        await msg.channel.purge(limit=number)


    @app_commands.command(name='nickname', description="Change a member's nickname")
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff, role_ids.owner)
    async def nickname(self, msg: discord.Interaction, target: discord.Member, nickname: str):
        if not target.nick:
            await target.edit(nick=nickname)
        elif target.nick.startswith('#'):
            number = target.nick.split(' ', 1)[0].strip()
            await target.edit(nick=f'{number} {nickname}')
        else:
            await target.edit(nick=nickname)

        await msg.response.send_message(embed=utils.embed_success(f'Modified nickname: {target.name}'))

    @app_commands.command(name='role', description="Modify member's roles[Admin]")
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff, role_ids.owner)
    async def role(self, msg: discord.Interaction, target: discord.Member, role1: discord.Role, role2: Optional[discord.Role]):

        message = f'Modified {target.name}:'

        if role1 in target.roles:
            await target.remove_roles(role1)
            message += f" -{role1.name}"
        else:
            await target.add_roles(role1)
            message += f" +{role1.name}"

        if role2:
            if role2 in target.roles:
                await target.remove_roles(role2)
                message += f" -{role2.name}"
            else:
                await target.add_roles(role2)
                message += f" +{role2.name}"

        await msg.response.send_message(embed=utils.embed_success(message))

    @app_commands.command(name='streams', description="List streams for a given heat[Admin]")
    @app_commands.checks.has_any_role(role_ids.admin, role_ids.staff, role_ids.owner)
    @app_commands.choices(race=[
        app_commands.Choice(name='D1', value='D1'),
        app_commands.Choice(name='D2 + D3', value='D2 + D3'),
        app_commands.Choice(name='All', value='All'),
    ])
    async def streams(self, msg: discord.Interaction, race: app_commands.Choice[str]):
        db = mongo['RH']
        drivers_col = db['drivers']

        await msg.response.send_message('Processing...')

        heats = {
            'D1': {
                'H1': [],
                'H2': [],
                'H3': []
            },
            'D2': {
                'H1': [],
                'H2': [],
                'H3': []
            },
            'D3': {
                'H1': [],
                'H2': [],
                'H3': [],
                'H4': []
            }
        }

        drivers = drivers_col.find({})
        driver_role = get(msg.guild.roles, id=role_ids.driver)

        for member in msg.guild.members:
            try:
                if driver_role in member.roles:
                    # driver = drivers_col.find_one({'id': member.id})
                    driver = (list(filter(lambda d: d['id'] == member.id, drivers)))
                    if len(driver) > 0:
                        driver = driver[0]
                        pprint(driver)

                        if driver and 'stream' in driver and not driver['league'] == 'placement':
                            div = driver['league']

                            for heat in heats[div].keys():
                                if get(msg.guild.roles, id=role_ids.heats[div][heat]) in member.roles:
                                    pprint(driver['gt'])
                                    heats[div][heat].append(f"{driver['gt']} - {driver['stream']}")

            except Exception as er:
                pprint(er)
                await msg.channel.send_message(embed=utils.embed_failure(er))

        try:
            embed = discord.Embed(
                title="Stream links:",
                color=15879747
            )

            if race.value == 'D1' or race.value == 'All':
                for heat in heats['D1'].keys():
                    if len(heats['D1'][heat]) > 0:
                        embed.add_field(name=f"D1 {heat}", value='\n'.join(heats['D1'][heat]), inline=False)

            if race.value == 'D2 + D3' or race.value == 'All':
                for heat in heats['D2'].keys():
                    if len(heats['D2'][heat]) > 0:
                        embed.add_field(name=f"D2 {heat}", value='\n'.join(heats['D2'][heat]), inline=False)
                for heat in heats['D3'].keys():
                    if len(heats['D3'][heat]) > 0:
                        embed.add_field(name=f"D3 {heat}", value='\n'.join(heats['D3'][heat]), inline=False)

        except Exception as er:
            pprint(er)
            await msg.channel.send_message(embed=utils.embed_failure(er))

        await msg.edit_original_response(content='', embed=embed)


async def setup(bot):
    await bot.add_cog(Administration(bot), guilds=[discord.Object(id=1077859376414593124)])




