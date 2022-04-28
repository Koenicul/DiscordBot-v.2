from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
from discord.ext.commands import CommandNotFound
import json
from random import choice

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

DISCORD_TOKEN = os.getenv("Discord_Token")
PREFIX = os.getenv("Prefix")

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True, help_command = help_command)

@bot.event
async def on_ready():
    print("logged in as {}".format(bot.user.name))

@bot.event
async def on_command_error(error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@bot.event
async def on_message(message):
    with open("bullied_users.json", "r") as f:
        data=json.load(f)
    for user in data:
        if user == message.author.id:
            sentence = message.content
            new_sentence = ''.join(choice((str.upper, str.lower))(c) for c in sentence)
            await message.channel.send(new_sentence)
    await bot.process_commands(message)

bot.load_extension("cmds.Spam")
bot.load_extension("cmds.Uploader")
bot.load_extension("cmds.Battle")
bot.run(DISCORD_TOKEN)