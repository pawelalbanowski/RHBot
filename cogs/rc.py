import discord
from typing import Optional
from discord.ext import commands
from discord import app_commands
from pprint import pprint
from cogs.misc import utils
from cogs.misc.roles import Roles
from cogs.misc.connections import mongo
from discord.utils import get
from cogs.misc.gsheetio import update_rc


role_ids = Roles()


class RC(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pprint('RC cog loaded')

    @commands.has_any_role(role_ids.staff, role_ids.admin, role_ids.owner)
    @commands.command()
    async def sync_rc(self, ctx) -> None:
        try:
            synced = await ctx.bot.tree.sync(guild=discord.Object(id=1077859376414593124))
            await ctx.send(f"synced {len(synced)} RC commands")
        except discord.HTTPException as er:
            await ctx.send(er)

    @app_commands.command(name='rc_submit', description='Submit a clip to Race Control')
    @app_commands.describe(link='Enter the full link (for example https://www.twitch.tv/racinghaven/clip/FancyGrossCroq...)')
    @app_commands.checks.has_role(role_ids.driver)
    async def rc_submit(self, msg: discord.Interaction, link: str, lap: int):
        db = mongo['RH']

        drivers_col = db['drivers']

        await msg.response.send_message(f'Processing...')

        driver = drivers_col.find_one({'id': msg.user.id})
        # div = None
        # heat = None

        split = None

        if get(msg.user.roles, id=role_ids.split1):
            split = '1'
        elif get(msg.user.roles, id=role_ids.split2):
            split = '2'
        elif get(msg.user.roles, id=role_ids.split3):
            split = '3'
        elif get(msg.user.roles, id=role_ids.split4):
            split = '4'

        # for d in role_ids.heats.keys():
        #     for h in role_ids.heats[d].keys():
        #         if get(msg.user.roles, id=role_ids.heats[d][h]):
        #             div = d
        #             heat = h




        if split:
            rc = {
                'gt': driver['gt'],
                'link': link,
                # 'heat': heat[1],
                'lap': lap,
                'split': split
            }

            db[f'RC_S{split}'].insert_one(rc)

            await msg.edit_original_response(content='',
                                             embed=utils.embed_success(
                                                 f'Clip submitted'))

    @app_commands.command(name='rc_sync', description='Sync RC with the sheet [Admin]')
    @app_commands.checks.has_role(role_ids.driver)
    async def rc_sync(self, msg: discord.Interaction):
        db = mongo['RH']

        await msg.response.send_message(f'Processing...')

        clips = {
            'S1': [],
            'S2': [],
            'S3': [],
            'S4': []
        }

        for d in range(1, 5):
            div_clips = db[f'RC_S{d}'].find({})
            if div_clips:
                div_clips = sorted(div_clips, key=lambda x: x['lap'])
                div_clips = list(map((
                    lambda a: [a['gt'], a['lap'], a['link']]
                 ), div_clips))

                clips[f'S{d}'] = div_clips

        update_rc(0, clips)


        await msg.edit_original_response(
            content='',
            embed=utils.embed_success('Synced!')
        )


async def setup(bot):
    await bot.add_cog(RC(bot), guilds=[discord.Object(id=1077859376414593124)])