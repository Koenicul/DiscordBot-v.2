from discord.ext import commands
import db
from sqlalchemy.orm import sessionmaker
import discord

Session = sessionmaker(bind=db.engine)
session = Session()

@commands.command(name="Inventory", help="List all items in your inventory")
async def Inventory(ctx):
    player = session.query(db.Player).filter(db.Player.id == ctx.author.id).first()
    if player is not None:
        if player.playerItems is not None:
            embed = discord.Embed(title="Inventory", description="Here are your items:", color=0x00ff00)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            for item in player.playerItems:
                embed.add_field(name=f"{item.item.name}:", value=f"{item.item.description}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You don't have any items")
    else:
        await ctx.send("You have no player")

def setup(bot):
    bot.add_command(Inventory)