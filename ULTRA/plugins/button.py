# madboy482
# designed for UltraX

import os
import re

from telethon import Button, events
from ..utils import admin_cmd
from ..utils import edit_or_reply, eor
from ..utils import sudo_cmd
from .. import CMD_HELP

BOT_USERNAME = Var.TG_BOT_USER_NAME_BF_HER

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")


@borg.on(admin_cmd(pattern=r"cbutton ?(.*)", outgoing=True))
@borg.on(sudo_cmd(pattern=r"cbutton ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    if reply_message:
        markdown_note = reply_message.text
    else:
        markdown_note = "".join(event.text.split(maxsplit=1)[1:])
    if not markdown_note:
        return await edit_delete(event, "**What text should I use in button post?**")
    prev = 0
    note_data = ""
    buttons = []
    for match in BTN_URL_REGEX.finditer(markdown_note):
        # Check if btnurl is escaped
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1
        # if even, not escaped -> create button
        if n_escapes % 2 == 0:
            # create a thruple with button label, url, and newline status
            buttons.append((match.group(2), match.group(3), bool(match.group(4))))
            note_data += markdown_note[prev : match.start(1)]
            prev = match.end(1)
        # if odd, escaped -> move along
        elif n_escapes % 2 == 1:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
        else:
            break
    else:
        note_data += markdown_note[prev:]
    message_text = note_data.strip() or None
    tl_ib_buttons = build_keyboard(buttons)
    tgbot_reply_message = None
    if reply_message and reply_message.media:
        tgbot_reply_message = await event.client.download_media(reply_message.media)
    if tl_ib_buttons == []:
        tl_ib_buttons = None
    await tgbot.send_message(
        entity=event.chat_id,
        message=message_text,
        parse_mode="html",
        file=tgbot_reply_message,
        link_preview=False,
        buttons=tl_ib_buttons,
    )
    await event.delete()
    if tgbot_reply_message:
        os.remove(tgbot_reply_message)
        
        
CMD_HELP.update(
    {
        "button": f"**Plugin : **`button`\
    \n\n**Button post helper**\
    \n•  **Syntax : **`.cbutton`\
    \n•  **Function :** __For working of this, you need your bot({BOT_USERNAME}) in the group/channel where you are using the command and Buttons must be in the format as [Name on button]<buttonurl:link you want to open> and markdown is Default to html__\
    \n•  **Example :** `.cbutton Test [Google]<buttonurl:https://www.google.com> [UltraX Chat]<buttonurl:https://t.me/ULTRAXCHAT:same> [UltraX]<buttonurl:https://t.me/UltraXOT>`\
    "
    }
)
