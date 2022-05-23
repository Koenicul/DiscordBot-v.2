from discord.ext import commands
import db
from sqlalchemy.orm import sessionmaker
from random import choice
import discord

Session = sessionmaker(bind=db.engine)
session = Session()

class Bully(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        for player in session.query(db.Bullied).all():
            if message.author.id == player.player_id:
                sentence = message.content
                new_sentence = ''.join(choice((str.upper, str.lower))(c) for c in sentence)
                await message.channel.send(new_sentence)

    @commands.command(name="AddBullied", help="Add a player to the list of players that will be bullied")
    async def AddBullied(self, ctx, player: discord.Member):
        exists = session.query(db.Bullied).filter(db.Bullied.player_id == player.id).first()
        if exists is None:
            session.add(db.Bullied(player_id=player.id))
            session.commit()
            await ctx.send(f"Added {player.display_name} to the list of players to be bullied")
        else:
            await ctx.send(f"{player.display_name} is already on the list of players to be bullied")

    @commands.command(name="RemoveBullied", help="Remove a player from the list of players that will be bullied")
    async def RemoveBullied(self, ctx, player: discord.Member):
        exists = session.query(db.Bullied).filter(db.Bullied.player_id == player.id).first()
        if exists is not None:
            session.query(db.Bullied).filter(db.Bullied.player_id==player.id).delete()
            session.commit()
            await ctx.send(f"Removed {player.display_name} from the list of players to be bullied")
        else:
            await ctx.send(f"{player.display_name} is not on the list of players to be bullied")

def setup(bot):
    bot.add_cog(Bully(bot))