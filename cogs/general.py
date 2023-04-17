import discord
from typing import Optional
from discord.ext import commands
from discord import app_commands
from pprint import pprint
from cogs.misc import utils
from cogs.misc.roles import Roles
from cogs.misc.connections import mongo
from discord.utils import get


role_ids = Roles()


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('General cog loaded')

    @commands.has_any_role(role_ids.staff, role_ids.admin, role_ids.owner)
    @commands.command()
    async def sync_general(self, ctx) -> None:
        try:
            synced = await ctx.bot.tree.sync(guild=discord.Object(id=1077859376414593124))
            await ctx.send(f"synced {len(synced)} General commands")
        except discord.HTTPException as er:
            await ctx.send(er)


    @app_commands.command(name='inrole', description='See list of members with role(s)')
    async def inrole(self, msg: discord.Interaction, role1: discord.Role, role2: Optional[discord.Role]):
        return

    @app_commands.checks.has_any_role(role_ids.member, role_ids.driver)
    @app_commands.command(name='quali', description='Get a list of drivers in said quali heat')
    @app_commands.choices(session=[
        app_commands.Choice(name='1', value='Q-1'),
        app_commands.Choice(name='2', value='Q-2'),
        app_commands.Choice(name='3', value='Q-3'),
        app_commands.Choice(name='4', value='Q-4'),
        app_commands.Choice(name='5', value='Q-5'),
        app_commands.Choice(name='6', value='Q-6'),
        app_commands.Choice(name='7', value='Q-7'),
        app_commands.Choice(name='8', value='Q-8'),
        app_commands.Choice(name='9', value='Q-9'),
    ])
    async def quali(self, msg: discord.Interaction, session: app_commands.Choice[str]):
        db = mongo['RH']
        drivers_col = db['drivers']

        gamertags = {
            'D1': [],
            'D2': [],
            'D3': []
        }

        await msg.response.send_message('Processing...')

        session_role = get(msg.guild.roles, id=role_ids.quali[session.value])

        for member in msg.guild.members:
            if session_role in member.roles:
                driver = drivers_col.find_one({'id': member.id})
                if driver:
                    gamertags[driver['league']].append(f"{driver['gt']}\n")
        embed = discord.Embed(
            title=f"List of drivers in {session.value}",
            color=15879747
        )
        embed.add_field(name="D1", value=gamertags['D1'], inline=False)
        embed.add_field(name="D2", value=gamertags['D2'], inline=False)
        embed.add_field(name="D3", value=gamertags['D3'], inline=False)

        await msg.edit_original_response(content='', embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot), guilds=[discord.Object(id=1077859376414593124)])