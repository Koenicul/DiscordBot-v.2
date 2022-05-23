from discord.ext import commands
import db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db.engine)
session = Session()

async def create_player(ctx):
    exists = session.query(db.Player).filter(db.Player.id == ctx.author.id).first()
    if exists is None:
        player = db.Player(ctx.author.id, ctx.author.name, 50, 100, 1, 0, 100, 10, 1, 1)
        session.add(player)
        session.commit()

        await ctx.send("Player created!")
    else:
        await ctx.send("Player already exists")