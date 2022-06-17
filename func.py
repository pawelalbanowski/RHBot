from pprint import pprint
from drivers import register, unregister, pet, gnfos, nickname, role, addrole, removerole, swap, \
    nuke, give_role_to_everyone, resetnicknames, resetnickname, fh5, cruise
from utils import help_msg


# parse command
async def process_msg(msg):
    roles = list(map((lambda a: a.name), msg.author.roles))
    
    # commands avaliable to everyone
    if msg.content.strip().startswith('.fh5') or msg.content.strip().startswith('.cancer'):
        await fh5(msg)
    if msg.content.strip().startswith('.pet'):
        await pet(msg)
    if msg.content.strip().startswith('.gnfos'):
        await gnfos(msg)
    if msg.content.strip().startswith('.cruise'):
        await cruise(msg)
    if msg.content.startswith('.help'):
        await help_msg(msg, roles)

    # only for drivers/admins 
    if msg.content.startswith('.swap ') and msg.channel.id == 985977023128281148:
        await swap(msg, roles)
        
    # only for viewers/admins
    if msg.content.startswith('.register ') and msg.channel.id == 985977023128281148:
        await register(msg, roles)
       
    # only for admins
    if 'Admin' in roles:
        if msg.content.startswith('.unregister '):
            await unregister(msg, roles)
            
        if msg.content.startswith('.nickname '):
            await nickname(msg, roles)
            
        if msg.content.startswith('.resetnickname '):
            await resetnickname(msg, roles)
            
        # modify user's roles
        if msg.content.startswith('.role '):
            await role(msg, roles)
            
        # add role to all mentioned ppl
        if msg.content.startswith('.addrole '):
            await addrole(msg, roles)
            
        # remove role from all mentioned ppl
        if msg.content.startswith('.removerole '):
            await removerole(msg, roles)
            
        # remove a role from everyone
        if msg.content.startswith('.nuke '):
            await nuke(msg, roles)
            
        # give role to everyone
        if msg.content.startswith('.give_role_to_everyone'):
            await give_role_to_everyone(msg, roles)
            
        # unsafe command so keep commented
        # if msg.content.startswith('.resetnicknames'):
            # await resetnicknames(msg, roles)
    return 



