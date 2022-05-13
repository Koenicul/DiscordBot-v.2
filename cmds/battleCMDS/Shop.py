import json
from discord.ext import commands
import discord

data = {}
items = {}

try:
    with open('battle_users.json', 'r') as f:
        data = json.load(f)
except:
    with open('battle_users.json', 'w') as jsonFile:
        json.dump(data, jsonFile)

def save():
    with open('battle_users.json', 'w') as f:
        f.write(json.dumps(data))

@commands.command(name="Shop", help="Open shop menu")
async def Shop(ctx):
    try:
        with open('items.json', 'r') as f:
            items = json.load(f)
    except:
        with open('items.json', 'w') as jsonFile:
            json.dump(items, jsonFile)
    await ctx.send("Opened Shop")
    embed = discord.Embed(title="Shop", description="Welcome to the shop!", color=discord.Color.orange())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name="Items", value="Here are the items you can buy:", inline=False)
    index = 1
    for i in items:
        description = items[i]["description"]
        price = items[i]["price"]
        embed.add_field(name=f"({index}) " + items[i]["name"] + ":", value=f"{description}\n${price}", inline=False)
        index += 1
    embed.set_footer(text="Use --Buy <item index> to buy an item")
    await ctx.send(embed=embed)

@commands.command(name="Buy", help="Buy an item")
async def Buy(ctx, item: int):
    try:
        with open('items.json', 'r') as f:
            items = json.load(f)
    except:
        with open('items.json', 'w') as jsonFile:
            json.dump(items, jsonFile)
    if 0 < item <= len(items):
        if str(ctx.author.id) in data:
            print("test2")
            if data[str(ctx.author.id)]["gold"] >= items[str(item)]["price"]:
                data[str(ctx.author.id)]["gold"] -= items[str(item)]["price"]
                data[str(ctx.author.id)]["items"].append(str(item))
                await ctx.send("Bought " + items[str(item)]["name"])
                save()
            else:
                await ctx.send("You don't have enough gold!")

def setup(bot):
    bot.add_command(Shop)
    bot.add_command(Buy)