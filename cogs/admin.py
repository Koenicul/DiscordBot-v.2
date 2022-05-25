from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import os
import db
from sqlalchemy.orm import sessionmaker
import discord

Session = sessionmaker(bind=db.engine)
session = Session()

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="AddItem", help="Adds an item to the database")
    async def addItem(self, ctx, name: str, description: str, price: int, type: str, effect: float):
        if ctx.author.id == int(os.getenv("Owner_id")):
            item = db.Item(name, description, price, type, effect)
            session.add(item)
            session.commit()

            embed = discord.Embed(title=f"({item.id}) {name}", description=f"Desciption: {description}\nPrice: ${str(price)}\nType: {type}\nEffect: {str(effect)}", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="You don't have the permissions to use this command", color=0xff0000)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))