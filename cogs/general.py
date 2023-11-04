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

    @commands.command()
    async def read(self, ctx) -> None:
        await ctx.send(f"https://test-english.com/reading/")

    @commands.command()
    async def drift(self, ctx) -> None:
        await ctx.send(f"I  am find team 👥 in Forza Horizon  my favorite 😍 car 🚚 is TOYOTA TRUENO 1985, favorite 📺🔥 type 📝📝 driving 🚗🚕 drift, level 🎚 198, have car 90, year 📅 13, 😏😏 device 💾 is wheel 🎡 Logitech G923, my target find 👀 team for drift 1 or 2 🕝 people, play without microphone, my tune TOYOTA  TRUENO 1985 is stage 🔮 A 800 top speed 🏃‍♀ 316.2 km/h 0-100 kph 10.449 power 🔋🔋 478 hp weight ⚖ 862 kg lateral gs 1.05 suspension Drift type 💻 compound Drift drivetrain RWD")

    @commands.command()
    async def gpt(self, ctx) -> None:
        await ctx.send(f"I will carefully consider it and you will have a response in 24 hours.")

    @commands.command()
    async def rhec(self, ctx) -> None:
        await ctx.send(f"https://discord.com/channels/1077859376414593124/1089346179504017418")

    @commands.command()
    async def cruise(self, ctx) -> None:
        await ctx.send(f"""Cruise 🚣‍♀ Rules:

No 😣 slamming into 🔝⚠️ convoy members. 

👨👨 No 🤑🤑🥳 racing 🐎 on cruises. 
No 🚫 drifting on cruises. 

Stay on 🧐 the road and stick 🏑 with convoy members while cruising. 

Hands 💛👇🏻🤞🏻✋🏻🤞🏻👍🏻👇🏻🤞🏻✋🏻 off 📴 controller 🎮 or pedals while ⌚🙄 parked! 

You must 👫 be 👎😨 in ⛵⛵🇺🇸 stream to participate in 😩 Races and Cruising. 

No 😰 very 💁 large 🤪 vehicles in 🥺 cruises (Gurkha’s, Unimog’s, etc.) 📒 unless 💁 those types 🈯 of vehicles are part 〽 of the cruise 💕💖✨🧚🏻 theme. 

No drag and or drift cars. 🚖""")

    @commands.command()
    async def tune(self, ctx) -> None:
        await ctx.send(f"""To every 😹 asking 💬😭 for 👷 a tune: I 🌏 am 💨 a member of a competitive gaming team. 👥 After checking with the team 👥 leaders, it has 🤔👉 been 🚟 decided that 😠 I 👀👨 can 👁️ not ⚙️ share 📷 tunes due to the fact that it can invite the competition 🏇 to try 💪😥 and obtain 💰 crucial information 📚 about ✨ our racing strategies. In 👉 other words: 😋🍁 I am under 🌝 contract to not 😖 share any 🚘 information 💁 including 🙌 tunes because the person 💅 asking 💬😭 could 😶 be competition. 🏇 I deeply 😱 apologize for 🚣🏻 the inconvenience.""")

    @commands.command()
    async def rivals(self, ctx) -> None:
        await ctx.send(f"I’m ❌🚷🏡 top 🎩 10 🔟 in 🙌 multiple rivals leaderboards but ❌ yeah, 😜 sure, 👍🤘 it’s totally 😲 a skill 😤 issue. 🙅🏾 You 😀 didn’t ❌ even 🌃 read 👏 my ✨📝 comment, 😋 did 🏿👏 you? 👈 How 👏 about 🌈 you 👉😩👨 come 🌚👽❤️ back 🧑🏿 when 👀⏰ you 🤓 have ⭐👏 something 😅 worthwhile to contribute to the conversation. 🤐  jfc This is why 😡 none 🙅🏻‍♀️ of the top 😌🥰🔝🏆 drivers interact with you 🆗 losers.  Edit: 📑 Adding proof, 📊📊 because 👲🏽 I 😍 know 🤔🙈 this community 😱 loves ❓ to circlejerk.")

    @commands.command()
    async def awbannt(self, ctx) -> None:
        await ctx.send(f"Ok. Awbannt. I'm going tuwu expwain thiws diwwigentwy. I knew thawt he was wacing in a gwoup. They fucked up awnd i ended up ovewtaking him. He was own my ass fow a wap awnd a hawf, gaining. I knew he was going tuwu pass. I was pwaying "passivewy" i didn't feew wike putting up a fight, especiawwy in the m8 against an wsw own kyawami. In spite of aww thawt, the fucking guy juwst knocks me out. He couwd have bewn mowe patient awnd passed without contact.")



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
                    gamertags[driver['league']].append(f"#{driver['nr']} {driver['gt']} ({member.mention})")
        embed = discord.Embed(
            title=f"List of drivers in {session.value}",
            color=15879747
        )
        embed.add_field(name="D1", value='\n'.join(gamertags['D1']), inline=False)
        embed.add_field(name="D2", value='\n'.join(gamertags['D2']), inline=False)
        embed.add_field(name="D3", value='\n'.join(gamertags['D3']), inline=False)

        await msg.edit_original_response(content='', embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot), guilds=[discord.Object(id=1077859376414593124)])