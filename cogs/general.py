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
import math


role_ids = Roles()


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('General cog loaded')

    @commands.has_any_role(role_ids.staff, role_ids.admin)
    @commands.command()
    async def sync_general(self, ctx) -> None:
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"synced {len(synced)} General commands")
        return


    @commands.hybrid_command(name='inrole', description='Use this command to find users in a role')
    @app_commands.describe(role='Enter the role or find it within the menu')
    async def _inrole(self, ctx, role: discord.Role):
        server = ctx.message.guild
        role_name = role
        role_id = server.roles[0]
        for role in server.roles:
            if role_name == role:
                role_id = role
                break
        else:
            await ctx.reply(f"That role does not exist!")
            return
        n = 0
        members = []
        for member in server.members:
            if role_id in member.roles:
                n += 1
                name = f"`{member.id}` " + member.name + "#" + member.discriminator + "\n"
                members.append(name)
        composite_members = [members[x:x + 20] for x in range(0, len(members), 20)]
        pages = []
        i = 1
        for elements in composite_members:
            string = ""
            for element in elements:
                string = string + element
            embedVar = discord.Embed(title=f"List of users in **{role}** role ({n})", description=string, colour=0x2ecc71)
            embedVar.set_footer(text=f"Page: {i} / {math.ceil(n / 20)}")
            # embedVar.add_field(name=f"Page #{i}", value=string)
            pages.append(embedVar)
            i += 1

        def predicate(message, l, r):
            def check(reaction, user):

                if reaction.message.id != message.id or user == self.bot.user:
                    return False
                if l and reaction.emoji == "⏪":
                    return True
                if r and reaction.emoji == "⏩":
                    return True
                return False

            return check

        page = 0
        left = "⏪"
        right = "⏩"

        while True:
            msg = await ctx.send(embed=pages[page])
            l = page != 0
            r = page != len(pages) - 1
            if l:
                await msg.add_reaction(left)
            if r:
                await msg.add_reaction(right)

            react = await self.bot.wait_for('reaction_add', check=predicate(msg, l, r))

            if str(react[0]) == left:
                page -= 1
            elif str(react[0]) == right:
                page += 1

            await msg.delete()

async def setup(bot):
    await bot.add_cog(General(bot), guilds=[discord.Object(id=875740357055352833)])