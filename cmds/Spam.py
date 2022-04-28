from discord.ext import commands
import os

@commands.command(name="Spam", help="Spam a message")
async def Spam(ctx):
    if ctx.message.author.name == os.getenv("Owner_id"):
        txt = open("test.txt", "r")
        split = txt.read().split()
        for i in split:
            await ctx.send("@everyone " + i)
    else:
        await ctx.send(ctx.message.author.name + " is noob!!!")

def setup(bot):
    bot.add_command(Spam)