from pprint import pprint
from drivers import register, unregister, pet, gnfos, nickname, role, addrole, removerole, swap, \
    nuke, give_role_to_everyone, resetnicknames, resetnickname, fh5, cruise


# parse command
async def process_msg(msg):
    roles = list(map((lambda a: a.name), msg.author.roles))
    if msg.content.startswith('.fh5') or msg.content.startswith('.cancer'):
        await fh5(msg)
    if msg.content == '.pet':
        await pet(msg)
    if msg.content == '.gnfos':
        await gnfos(msg)
    if msg.content == '.cruise':
        await cruise(msg)
    if 'Admin' in roles:
        if msg.content.startswith('.register '):
            await register(msg, roles)
        if msg.content.startswith('.unregister '):
            await unregister(msg, roles)
        if msg.content.startswith('.nickname '):
            await nickname(msg, roles)
        # modify user's roles
        if msg.content.startswith('.role '):
            await role(msg, roles)
        # add role to all mentioned ppl
        if msg.content.startswith('.addrole '):
            await addrole(msg, roles)
        # remove role from all mentioned ppl
        if msg.content.startswith('.removerole '):
            await removerole(msg, roles)
        # swap car
        if msg.content.startswith('.swap '):
            await swap(msg, roles)
        # remove a role from everyone
        if msg.content.startswith('.nuke '):
            await nuke(msg, roles)
        # give role to everyone
        if msg.content.startswith('.give_role_to_everyone'):
            await give_role_to_everyone(msg, roles)
        if msg.content.startswith('.resetnicknames'):
            await resetnicknames(msg, roles)
        if msg.content.startswith('.resetnickname '):
            await resetnickname(msg, roles)
    return



