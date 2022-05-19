from discord.ext import commands
import db
from sqlalchemy.orm import sessionmaker
import discord

Session = sessionmaker(bind=db.engine)
session = Session()

@commands.command(name="Daily", Help="Get your daily reward")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def Daily(ctx):
    player = session.query(db.Player).filter(db.Player.id == ctx.author.id).first()
    if player is not None:
        player.gold += 100
        session.commit()
        await ctx.send("You got 100 gold!")
    else:
        await ctx.send("You have no player")

@Daily.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        time = convert(error.retry_after)
        embed = discord.Embed(title=f"You are in cooldown",description=f"Try again in {time}.", color=discord.Color.orange())
        await ctx.send(embed=embed)

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def setup(bot):
    bot.add_command(Daily)