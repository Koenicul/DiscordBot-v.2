from discord.ext import commands
import db
from sqlalchemy.orm import sessionmaker
import discord

Session = sessionmaker(bind=db.engine)
session = Session()

async def shop(ctx):
    await ctx.send("Opened Shop")
    embed = discord.Embed(title="Shop", description="Welcome to the shop!", color=discord.Color.orange())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name="Items", value="Here are the items you can buy:", inline=False)
    for s in session.query(db.Item).all():
        embed.add_field(name=f"({s.id}) {s.name}:", value=f"{s.description}\n${s.price}", inline=False)
    embed.set_footer(text="Use --Buy <item index> to buy an item")
    await ctx.send(embed=embed)

async def buy(ctx, index: int):
    player = session.query(db.Player).filter(db.Player.id == ctx.author.id).first()
    if 0 < index <= session.query(db.Item).count() and player is not None:
        item = session.query(db.Item).filter(db.Item.id == index).first()
        if player.gold >= item.price:
            player.gold -= item.price

            player_item = db.PlayerItem(player=player, item=item)
            session.add(player_item)
            session.commit()
            await ctx.send(f"Bought {item.name} for ${item.price}")
        else:
            await ctx.send("You don't have enough gold!")
    else:
        await ctx.send("Invalid item or you don't have a player!")