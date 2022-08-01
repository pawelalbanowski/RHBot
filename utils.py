import discord as dc
import asyncio


def embed(desc):
    return dc.Embed(
            description=":ballot_box_with_check: " + desc,
            color=15879747
        )


def divide_chunks(content, size):
    for i in range(0, len(content), size):
        yield content[i:i + size]


async def pages(cli, msg, content):
    el_count = len(content)
    contents = list(divide_chunks(content, 20))
    pages_num = len(contents)
    cur_page = 1
    message = await msg.reply(embed=embed(f"Page {cur_page}/{pages_num}, {el_count} elements:\n{' '.join(contents[cur_page-1])}"))
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == msg.author and str(reaction.emoji) in ["◀️", "▶️", '👍']
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await cli.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and cur_page != pages_num:
                cur_page += 1
                await message.edit(embed=embed(f"Page {cur_page}/{pages_num}, {el_count} elements:\n{' '.join(contents[cur_page-1])}"))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(embed=embed(f"Page {cur_page}/{pages_num}, {el_count} elements:\n{' '.join(contents[cur_page-1])}"))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == '👍':
                await message.delete()
                await msg.delete()

            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.delete()
            await msg.delete()
            break


def help_admin():
    message = dc.Embed(
        title="1Bot Help",
        description=":ballot_box_with_check: Commands avaliable to role: Admin",
        color=15879747
    )

    message.add_field(
        name=".help OR .help [role]",
        value="Displays this message / displays this message as seen for [role]",
        inline=False
    )

    message.add_field(
        name=".register [number], [gamertag], [car]",
        value="Driver registering themselves (avaliable only in #registration-requests)",
        inline=False
    )

    message.add_field(
        name=".purge",
        value="Clears channel of messages",
        inline=False
    )

    message.add_field(
        name=".clear [number]",
        value="Deletes [number] messages from channel",
        inline=False
    )

    message.add_field(
        name=".lock OR .unlock",
        value="Locks/unlocks channel",
        inline=False
    )

    message.add_field(
        name=".number",
        value=".number @mention value",
        inline=False
    )

    message.add_field(
        name=".inrole [role]",
        value="Displays list of members in [role]",
        inline=False
    )

    message.add_field(
        name=".register [@mention] [number], [gamertag], [car]",
        value="Admin registering [@mention]",
        inline=False
    )

    message.add_field(
        name=".unregister [@mention] [@mention]",
        value="Unregisters everyone mentioned",
        inline=False
    )

    message.add_field(
        name=".swap [car]",
        value="Swaps author to car [car] (avaliable only in #registration-requests)",
        inline=False
    )

    message.add_field(
        name=".swap [car] [@mention (driver)]",
        value="Swaps [@mention] to car [car] if it's avaliable (avaliable only in #registration-requests)",
        inline=False
    )

    message.add_field(
        name=".nickname [@mention] [nickname]",
        value="Modifies nickname of [@mention]",
        inline=False
    )

    message.add_field(
        name=".role [@mention] [role], [role]",
        value="Modifies roles of [@mention] (if has [role], removes, if doesn't, adds)",
        inline=False
    )

    message.add_field(
        name=".addrole [role], [@mention] [@mention]  OR  .removerole [role], [@mention] [@mention]",
        value="Adds or removes [role] from all mentioned people",
        inline=False
    )

    message.add_field(
        name=".nuke [role]",
        value="Removes [role] from every member",
        inline=False
    )

    message.add_field(
        name=".give_role_to_everyone [role]",
        value="Gives every member [role]",
        inline=False
    )

    message.add_field(
        name=".resetnicknames",
        value="Resets all nicknames (disabled)",
        inline=False
    )

    message.add_field(
        name=".resetnickname [@mention], [@mention]",
        value="Resets nicknames of everyone mentioned",
        inline=False
    )

    message.add_field(
        name=".pet",
        value="pets the bot :))",
        inline=False
    )

    message.add_field(
        name=".gnfos",
        value=":))",
        inline=False
    )

    message.add_field(
        name=".fh5 OR .cancer",
        value="displays information about fh5 :))",
        inline=False
    )

    message.add_field(
        name=".morb",
        value="lets you watch the best movie of all time",
        inline=False
    )

    return message


def help_member():
    message = dc.Embed(
        title="1Bot Help",
        description=":ballot_box_with_check: Commands avaliable to role: Member",
        color=15879747
    )

    message.add_field(
        name=".help",
        value="Displays this message",
        inline=False
    )

    message.add_field(
        name=".inrole [role]",
        value="Displays list of members in [role]",
        inline=False
    )

    message.add_field(
        name=".register [number], [gamertag], [car]",
        value="Driver registering themselves (avaliable only in #registration-requests)",
        inline=False
    )

    message.add_field(
        name=".pet",
        value="pets the bot :))",
        inline=False
    )

    message.add_field(
        name=".gnfos",
        value=":))",
        inline=False
    )

    message.add_field(
        name=".fh5 OR .cancer",
        value="displays information about fh5 :))",
        inline=False
    )

    message.add_field(
        name=".morb",
        value="lets you watch the best movie of all time",
        inline=False
    )

    return message


def help_driver():
    message = dc.Embed(
        title="1Bot Help",
        description=":ballot_box_with_check: Commands avaliable to role: Driver",
        color=15879747
    )

    message.add_field(
        name=".help",
        value="Displays this message",
        inline=False
    )

    message.add_field(
        name=".inrole [role]",
        value="Displays list of members in [role]",
        inline=False
    )

    message.add_field(
        name=".swap [car]",
        value="Swaps author to car [car] (avaliable only in #registration-requests)",
        inline=False
    )

    message.add_field(
        name=".pet",
        value="pets the bot :))",
        inline=False
    )

    message.add_field(
        name=".gnfos",
        value=":))",
        inline=False
    )

    message.add_field(
        name=".fh5 OR .cancer",
        value="displays information about fh5 :))",
        inline=False
    )

    message.add_field(
        name=".morb",
        value="lets you watch the best movie of all time",
        inline=False
    )

    return message


async def embed_timeout(cli, msg, embed_obj):
    message = await msg.reply(embed=embed_obj)
    # getting the message object for editing and reacting

    def check(reaction, user):
        return user == msg.author and str(reaction.emoji) == '👍'
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await cli.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == '👍':
                await message.delete()
                await msg.delete()
        except asyncio.TimeoutError:
            await message.delete()
            await msg.delete()
            break


async def help_msg(cli, msg, roles):  # .help  OR .help [role]
    if 'Admin' in roles:
        if msg.content.strip() == '.help':
            await embed_timeout(cli, msg, help_admin())
        elif msg.content.strip() == '.help Driver':
            await embed_timeout(cli, msg, help_driver())
        elif msg.content.strip() == '.help Member':
            await embed_timeout(cli, msg, help_member())
    elif 'Driver' in roles:
        await embed_timeout(cli, msg, help_driver())
    elif 'Member' in roles:
        await embed_timeout(cli, msg, help_member())

