from discord.ext import commands
import db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db.engine)
session = Session()

@commands.command(name="CreatePlayer", help="Create a player")
async def CreatePlayer(ctx):
    exists = session.query(db.Player).filter(db.Player.id == ctx.author.id).first()
    print(exists)
    if exists is None:
        print("Creating player")
        player = db.Player(ctx.author.id, ctx.author.name, 100, 100, 1, 0, 100, 10, 1, 1)
        session.add(player)
        session.commit()

        await ctx.send("Player created!")
    else:
        print(exists.player_id)
        await ctx.send("Player already exists")

def setup(bot):
    bot.add_command(CreatePlayer)