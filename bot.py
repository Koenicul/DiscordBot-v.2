from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
load_dotenv()
import os

DISCORD_TOKEN = os.getenv("Discord_Token")
PREFIX = os.getenv("Prefix")

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True, help_command=help_command, intents=intents)

@bot.command(name="Load", help="Loads a cog")
async def Load(ctx, extention):
    bot.load_extension(f'cogs.{extention}')
    await ctx.send(f'Loaded {extention}')

@bot.command(name="Unload", help="Unloads a cog")
async def Unload(ctx, extention):
    bot.unload_extension(f'cogs.{extention}')
    await ctx.send(f'Unloaded {extention}')

@bot.command(name="Reload", help="Reloads a cog or all cogs")
async def Reload(ctx, extention):
    if extention == "all":
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.unload_extension(f'cogs.{filename[:-3]}')
                bot.load_extension(f'cogs.{filename[:-3]}')
        return await ctx.send("Reloaded all cogs")
    bot.unload_extension(f'cogs.{extention}')
    bot.load_extension(f'cogs.{extention}')
    await ctx.send(f'Reloaded {extention}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(DISCORD_TOKEN)
