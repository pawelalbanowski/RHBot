from pprint import pprint
from drivers import Driver
from members import Member
from admins import Admin
from utils import help_msg


# parse command
async def process_msg(msg, cli):
    roles = list(map((lambda a: a.name), msg.author.roles))

    # commands avaliable to everyone
    if msg.content.strip().startswith('.fh5') or msg.content.strip().startswith('.cancer'):
        await Member.fh5(msg)

    if msg.content.strip().startswith('.pet'):
        await Member.pet(msg)

    if msg.content.strip().startswith('.gnfos'):
        await Member.gnfos(msg)

    if msg.content.strip().startswith('.cruise'):
        await Member.cruise(msg)

    if msg.content.startswith('.help'):
        await help_msg(cli, msg, roles)

    if msg.content.startswith('.inrole'):
        await Member.inrole(msg, cli)

    if msg.content.startswith('.morb'):
        await msg.reply('https://cdn.discordapp.com/attachments/942849742927458374/987448991425888276/morbius.webm')

    # only for drivers/admins 
    if msg.content.startswith('.swap ') and msg.channel.id == 985977023128281148:
        await Driver.swap(msg, roles)

    # only for viewers/admins
    if msg.content.startswith('.register ') and msg.channel.id == 985977023128281148:
        await Driver.register(msg, roles)

    # only for admins
    if 'Admin' in roles:
        if msg.content.startswith('.clear'):
            await Admin.clear(cli, msg)

        if msg.content.startswith('.purge'):
            await Admin.purge(msg, roles)

        if msg.content.startswith('.unregister '):
            await Admin.unregister(msg, roles)

        if msg.content.startswith('.nickname '):
            await Admin.nickname(msg, roles)

        if msg.content.startswith('.resetnickname '):
            await Admin.resetnickname(msg, roles)

        # modify user's roles
        if msg.content.startswith('.role '):
            await Admin.role(msg, roles)

        # add role to all mentioned ppl
        if msg.content.startswith('.addrole '):
            await Admin.addrole(msg, roles)

        # remove role from all mentioned ppl
        if msg.content.startswith('.removerole '):
            await Admin.removerole(msg, roles)

        # remove a role from everyone
        if msg.content.startswith('.nuke '):
            await Admin.nuke(msg, roles)

        # give role to everyone
        if msg.content.startswith('.give_role_to_everyone'):
            await Admin.give_role_to_everyone(msg, roles)

        # unsafe command so keep commented
        # if msg.content.startswith('.resetnicknames'):
        # await Admin.resetnicknames(msg, roles)
    return
