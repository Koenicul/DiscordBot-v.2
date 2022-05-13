import json
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import os

items = {}

try:
    with open('items.json', 'r') as f:
        items = json.load(f)
except:
    with open('items.json', 'w') as jsonFile:
        json.dump(items, jsonFile)

def save():
    with open('items.json', 'w') as f:
        f.write(json.dumps(items))

@commands.command(name="addItem", help="bruh")
async def addItem(ctx, name, description, price, effectType, effect):
    if ctx.message.author.name == os.getenv("Owner_id"):
        items[len(items)+1] = {"name": name, "description": description, "price": int(price), "effectType": effectType, "effect": effect}
        await ctx.send("Added item\nName: " + name + "\nDescription: " + description + "\nPrice: $" + price + "\nEffectType: " + effectType + "\nEffect: " + effect)
        save()

def setup(bot):
    bot.add_command(addItem)