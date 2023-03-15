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


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('General cog loaded')

    @commands.has_any_role(role_ids.staff, role_ids.admin, role_ids.owner)
    @commands.command()
    async def sync_general(self, ctx) -> None:
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"synced {len(synced)} General commands")
        return


    @app_commands.command(name='inrole', description='See list of members with role(s)')
    async def inrole(self, msg: discord.Interaction, role1: discord.Role, role2: Optional[discord.Role]):
        return


async def setup(bot):
    await bot.add_cog(General(bot), guilds=[discord.Object(id=1077859376414593124)])