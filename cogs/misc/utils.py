import discord
import asyncio
import re


# class Buttons(discord.ui.View):
#     def __init__(self) -> None:
#         super().__init__(timeout=None)
#
#     @discord.ui.button(label="<-", style=discord.ButtonStyle.grey, custom_id="back")
#     async def back(self, msg: discord.Interaction, button: discord.ui.Button):

def ms_to_laptime(ms):
    if ms == 0:
        return 0
    time = ""
    time += str(ms // 60000) + ":"
    ms -= str(ms // 60000) * 60000
    time += str(ms // 1000) + "."
    ms -= str(ms // 1000) * 1000
    if ms == 0:
        time += f"000"
    elif len(str(ms)) == 1:
        time += f"00{str(ms)}"
    elif len(str(ms)) == 2:
        time += f"0{str(ms)}"

    return time


def find_re(elements, key):
    occurences = 0
    found = None
    for el in elements:
        if el.lower() == key.lower():
            return el
        if re.search(key, el, re.IGNORECASE):
            occurences += 1
            found = el
    if occurences == 1:
        return found
    return False


def embed_success(desc):
    return discord.Embed(
            description=":ballot_box_with_check: " + desc,
            color=15879747
        )


def embed_failure(desc):
    return discord.Embed(
            description=":x: " + desc,
            color=15879747
        )


def divide_chunks(content, size):
    for i in range(0, len(content), size):
        yield content[i:i + size]


async def pages(cli, msg, content, title):
    el_count = len(content)
    contents = list(divide_chunks(content, 20))
    pages_num = len(contents)
    cur_page = 1
    message = await msg.response.send_message(embed=embed_success(f"{title}\n**Page {cur_page}/{pages_num}, {el_count} elements:**\n{' '.join(contents[cur_page-1])}"))
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
                await message.edit(embed=embed_success(f"Page {cur_page}/{pages_num}, {el_count} elements:\n{' '.join(contents[cur_page-1])}"))
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(embed=embed_success(f"Page {cur_page}/{pages_num}, {el_count} elements:\n{' '.join(contents[cur_page-1])}"))
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