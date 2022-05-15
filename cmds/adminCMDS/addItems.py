import json
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import os

items = {}

@commands.command(name="addItem", help="bruh")
async def addItem(ctx, name, description, price, effectType, effect):
    try:
        with open('items.json', 'r') as f:
            items = json.load(f)
    except:
        with open('items.json', 'w') as jsonFile:
            json.dump(items, jsonFile)

    if ctx.message.author.name == os.getenv("Owner_id"):
        items[len(items)+1] = {"name": name, "description": description, "price": int(price), "effectType": effectType, "effect": float(effect)}
        await ctx.send("Added item\nName: " + name + "\nDescription: " + description + "\nPrice: $" + price + "\nEffectType: " + effectType + "\nEffect: " + effect)
        with open('items.json', 'w') as f:
            f.write(json.dumps(items))
    else:
        await ctx.send("You don't have the permissions to use this command.")

def setup(bot):
    bot.add_command(addItem)