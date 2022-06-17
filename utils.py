import discord as dc


def embed(desc):
    return dc.Embed(
            description=":ballot_box_with_check: " + desc,
            color=15879747
        )


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

    return message


def help_viewers():
    message = dc.Embed(
        title="1Bot Help",
        description=":ballot_box_with_check: Commands avaliable to role: Viewers",
        color=15879747
    )

    message.add_field(
        name=".help",
        value="Displays this message",
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
    return message


def help_drivers():
    message = dc.Embed(
        title="1Bot Help",
        description=":ballot_box_with_check: Commands avaliable to role: Drivers",
        color=15879747
    )

    message.add_field(
        name=".help",
        value="Displays this message",
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
    return message


async def help_msg(msg, roles):  # .help  OR .help [role]
    if 'Admin' in roles:
        if msg.content.strip() == '.help':
            await msg.reply(embed=help_admin())
        elif msg.content.strip() == '.help Drivers':
            await msg.reply(embed=help_drivers())
        elif msg.content.strip() == '.help Viewers':
            await msg.reply(embed=help_viewers())
    elif 'Drivers' in roles:
        await msg.reply(embed=help_drivers())
    elif 'Viewers' in roles:
        await msg.reply(embed=help_viewers())

