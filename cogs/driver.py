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

# I DONT FUCKING UNDERSTAND WHY THIS DOES NOT SYNC AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# This is untested but should work nonetheless
class Driver(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('Driver cog loaded')

    @app_commands.checks.has_any_role(role_ids.staff, role_ids.admin)
    @commands.command()
    async def sync_driver(self, ctx) -> None:
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"synced {len(synced)} Driver commands")
        return


    @app_commands.command(name='quali', description='Check the attendees of a given quali heat')
    @app_commands.checks.has_any_role(role_ids.div_manager, role_ids.admin, role_ids.staff)
    @app_commands.describe(number='The Number Of The Quali Heat')
    async def quali(self, ctx, number: int):
        server = ctx.message.guild
        quali_role_id = role_ids.quali_specific(number)
        members = []
        for member in server.members:
            if quali_role_id in member.roles:
                n += 1
                for role in server.roles:
                    if role.id == utils.get_div_id_of_member(member, role_ids.leagues):
                        div = role.name
                        break
                name = f"{member.id} {member.name}#{member.discriminator}, {div} \n"
                members.append(name)
                members_d1 = [member for member in members if "D1" in member]
                members_d2 = [member for member in members if "D2" in member]
                members_d3 = [member for member in members if "D3" in member]
                members_sorted = members_d1 + members_d2 + members_d3
                pprint(members_sorted)
        embed = discord.Embed(title= f"Q{number} attendees", description=members_sorted, color=15879747)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Driver(bot), guilds=[discord.Object(id=875740357055352833)])

