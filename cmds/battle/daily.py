from discord.ext import commands
import db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db.engine)
session = Session()

async def daily(ctx):
    player = session.query(db.Player).filter(db.Player.id == ctx.author.id).first()
    if player is not None:
        player.gold += 100
        session.commit()
        await ctx.send("You got 100 gold!")
    else:
        await ctx.send("You have no player")

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)