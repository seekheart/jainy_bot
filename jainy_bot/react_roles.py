import os
import discord

role_message_id = int(os.environ.get("ROLE_MESSAGE_ID"))
if not role_message_id:
    raise AttributeError("ROLE_MESSAGE_ID not set!")


emoji_to_role = {
    discord.PartialEmoji(name='🍖'): 1197959991315927101,
    discord.PartialEmoji(name='🪦'): 800444883897942086,
    discord.PartialEmoji.from_str('<:pokeball:1199003145657909362>'): 1197962478726959266,
    discord.PartialEmoji.from_str('<:SeekMountUp:913166118452080692>'): 1197955990553903255,
    discord.PartialEmoji.from_str('<:jainaborb:536631923380977694>'): 1206258593893195797
}
