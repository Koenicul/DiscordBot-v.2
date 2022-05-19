from discord.ext import commands
import db
from sqlalchemy.orm import sessionmaker
import discord

Session = sessionmaker(bind=db.engine)
session = Session()
temp_items = []

@commands.command(name="Inventory", help="List all items in your inventory")
async def Inventory(ctx):
    player = session.query(db.Player).filter(db.Player.id == ctx.author.id).first()
    if player is not None:
        if player.playerItems is not None:
            embed = discord.Embed(title="Inventory", description="Here are your items:", color=0x00ff00)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            if len(player.equips) != 0:
                embed.add_field(name="Equipped:", value="Here are your equipped items:", inline=False)
                for item in player.equips:
                    embed.add_field(name=f"({item.id}) {item.item.name}:", value=f"{item.item.description}", inline=False)
            if len(player.playerItems) != 0:
                embed.add_field(name="Items:", value="Here are your items:", inline=False)
                for item in player.playerItems:
                    embed.add_field(name=f"({item.id}) {item.item.name}:", value=f"{item.item.description}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You don't have any items")
    else:
        await ctx.send("You have no player")

@commands.command(name="Equip", help="Equip an item")
async def Equip(ctx, index: int):
    player = session.query(db.Player).filter(db.Player.id == ctx.author.id).first()
    if player is not None and 0 < index <= len(player.playerItems):
        item = session.query(db.PlayerItem).filter(db.PlayerItem.id == index).first().item
        for equiped in session.query(db.Equipment).filter(db.Equipment.player == player):
            if equiped.item.type == "weapon" and item.type == "weapon":
                return await ctx.send("You already have a weapon equipped")
            elif equiped.item.type == "armor" and item.type == "armor":
                return await ctx.send("You already have an armor equipped")
            elif equiped.item.type == "boots" and item.type == "boots":
                return await ctx.send("You already have boots equipped")

        new_equip = db.Equipment(player=player, item=item)
        session.query(db.PlayerItem).filter(db.PlayerItem.id == index).delete()
        await pos_change_stats(player, item)
        session.add(new_equip)
        session.commit()
        await ctx.send(f"You equipped {item.name}")
        for item in player.playerItems:
            temp_items.append(item.item.id)
            session.query(db.PlayerItem).filter(db.PlayerItem.id == item.id).delete()
        session.commit()
        for item in temp_items:
            new_item = db.PlayerItem(player=player, item=session.query(db.Item).filter(db.Item.id == item).first())
            session.add(new_item)
        session.commit()
        temp_items.clear()
    else:
        return await ctx.send("You don't have that item or you don't have a player")

@commands.command(name="Unequip", help="Unequip an item")
async def Unequip(ctx, type: str):
    player = session.query(db.Player).filter(db.Player.id == ctx.author.id).first()
    if player is not None:
        for item in player.equips:
            if item.item.type == type:
                session.query(db.Equipment).filter(db.Equipment.id == item.id).delete()
                tItem = session.query(db.Item).filter(db.Item.id == item.item.id).first()
                player_item = db.PlayerItem(player=player, item=tItem)
                await neg_change_stats(player, tItem)
                session.add(player_item)
                session.commit()
                return await ctx.send(f"You unequipped {item.item.name}")
    else:
        return await ctx.send("You don't have a player")

async def pos_change_stats(player, item):
    if item.type == "weapon":
        player.attack += item.effect
    elif item.type == "armor":
        player.defense -= item.effect
    elif item.type == "boots":
        player.speed += item.effect

async def neg_change_stats(player, item):
    if item.type == "weapon":
        player.attack -= item.effect
    elif item.type == "armor":
        player.defense += item.effect
    elif item.type == "boots":
        player.speed -= item.effect
                
def setup(bot):
    bot.add_command(Inventory)
    bot.add_command(Equip)
    bot.add_command(Unequip)