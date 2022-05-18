from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import os
import db
from sqlalchemy.orm import sessionmaker
import discord

Session = sessionmaker(bind=db.engine)
session = Session()

@commands.command(name="addItem", help="bruh")
async def addItem(ctx, name: str, description: str, price: int, type: str, effect: float):
    if ctx.message.author.name == os.getenv("Owner_id"):
        item = db.Item(name, description, price, type, effect)
        session.add(item)
        session.commit()

        embed = discord.Embed(title=f"({item.id}) {name}", description=f"Desciption: {description}\nPrice: ${str(price)}\nType: {type}\nEffect: {str(effect)}", color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="You don't have the permissions to use this command", color=0xff0000)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(addItem)