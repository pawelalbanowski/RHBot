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
from bson.objectid import ObjectId


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
    @app_commands.describe(link='Enter the full link (for example https://www.twitch.tv/racinghaven/clip/FancyGrossCroq...)', involved="Tag the other person in the clip (or yourself if you're appealing an in game penalty)")
    @app_commands.checks.has_role(role_ids.driver)
    @app_commands.choices(type=[
        app_commands.Choice(name='Incident', value='incident'),
        app_commands.Choice(name='Appeal', value='appeal')
    ])
    async def rc_submit(self, msg: discord.Interaction, link: str, race: app_commands.Range[int, 1, 2], lap: int, involved: discord.Member, type: app_commands.Choice[str]):
        db = mongo['RH']

        drivers_col = db['drivers']

        await msg.response.send_message(f'Processing...')

        driver = drivers_col.find_one({'id': msg.user.id})
        driver2 = None
        
        if involved.id != msg.user.id:
            driver2 = drivers_col.find_one({'id': involved.id})
            if driver2:
                driver2 = driver2['gt']

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


        if driver2:
            gt = f"{driver['gt']}, {driver2}"
        else:
            gt = driver['gt']
            

        if split:
            rc = {
                'gt': gt,
                'link': link,
                'pov2': "",
                # 'heat': heat[1],
                'race': race,
                'lap': lap,
                'split': split,
                'type': type.value
            }

            result = db[f'RC_S{split}'].insert_one(rc)
            incident_id = str(result.inserted_id)
            
            
            response_embed = discord.Embed(
                title=f":ballot_box_with_check: Clip submitted by {msg.user.mention}",
                url=link,
                description=f"Incident ID: **{incident_id}**",
                color=15879747
            )
            
            if driver2:
                response_embed.add_field(name="",
                                         value=f"**Involved driver:** {involved.mention} ({driver2})")
                response_embed.add_field(name="", 
                                         value=f"You can add your POV using the **/rc_pov** command using the **Incident ID** (at the top of this message)")
            
            await msg.edit_original_response(content=f'',
                                                embed=response_embed)
                
                
    @app_commands.command(name='rc_pov', description='Submit a POV for an incident to Race Control')
    @app_commands.describe(id='Incident ID (from the incident message you were tagged in)', link='Enter the full link (for example https://www.twitch.tv/racinghaven/clip/FancyGrossCroq...)')
    @app_commands.checks.has_role(role_ids.driver)
    async def rc_pov(self, msg: discord.Interaction, id: str, link: str):
        db = mongo['RH']

        drivers_col = db['drivers']

        await msg.response.send_message(f'Processing...')

        driver = drivers_col.find_one({'id': msg.user.id})
        
        split = None

        if get(msg.user.roles, id=role_ids.split1):
            split = '1'
        elif get(msg.user.roles, id=role_ids.split2):
            split = '2'
        elif get(msg.user.roles, id=role_ids.split3):
            split = '3'
        elif get(msg.user.roles, id=role_ids.split4):
            split = '4'
        
        
        incident = db[f'RC_S{split}'].find_one({'_id': ObjectId(id)})
        
        
        if incident:
            db[f'RC_S{split}'].update_one({'_id': ObjectId(id)}, {'$set': {'pov2': link}})
            
            await msg.edit_original_response(content=f'',
                                                embed=utils.embed_success(
                                                    f'Clip for incident **{id}** submitted: {link}'))
            
        else:
            await msg.edit_original_response(content=f'',
                                                embed=utils.embed_failure(
                                                    f'Incident **{id}** not found, check the ID and try again'))

            

    @app_commands.command(name='rc_sync', description='Sync RC with the sheet [Admin]')
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

        update_rc(2, clips)


        await msg.edit_original_response(
            content='',
            embed=utils.embed_success('Synced!')
        )


async def setup(bot):
    await bot.add_cog(RC(bot), guilds=[discord.Object(id=1077859376414593124)])