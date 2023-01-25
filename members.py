# from typing import Optional
# import discord
# from discord.utils import get
# from utils import find_re, embed_success, embed_failure, pages
#
#
# async def inrole(client, msg, role1, role2: Optional[str]):
#     roles = list(map((lambda a: a.name), msg.guild.roles))
#     findrole1 = find_re(roles, role1)
#     findrole2 = None
#     if role2:
#         findrole2 = find_re(roles, role2)
#
#     if findrole2 is None:
#         role1_obj = get(msg.guild.roles, name=findrole1)
#         members_list = []
#
#         for member in msg.guild.members:
#             if role1_obj in member.roles:
#                 members_list.append(f'{member.name}\n')
#
#         if len(members_list) == 0:
#             return embed_failure(f'Found no members in role {role1}')
#
#         await pages(client, msg, members_list, f"**List of users in role: {role1}**")
#         return False


