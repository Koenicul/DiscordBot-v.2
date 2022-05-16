import json
from discord.ext import commands

data = {}
items = {}

@commands.command(name="ListItems", help="List all items in your inventory")
async def ListItems(ctx):
    try:
        with open('battle_users.json', 'r') as f:
            data = json.load(f)
    except:
        with open('battle_users.json', 'w') as jsonFile:
            json.dump(data, jsonFile)

    try:
        with open('items.json', 'r') as f:
            items = json.load(f)
    except:
        with open('items.json', 'w') as jsonFile:
            json.dump(items, jsonFile)

    if str(ctx.author.id) in data:
        if len(data[str(ctx.author.id)]["items"]) > 0:
            await ctx.send(f"{ctx.author.mention} has these items: " + ", ".join(items[i]["name"] for i in data[str(ctx.author.id)]["items"]) + ".")
        else:
            await ctx.send("You have no items")
    else:
        await ctx.send("You have no player")

def setup(bot):
    bot.add_command(ListItems)