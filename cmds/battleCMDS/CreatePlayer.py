import json
from discord.ext import commands

data = {}

try:
    with open('battle_users.json', 'r') as f:
        data = json.load(f)
except:
    with open('battle_users.json', 'w') as jsonFile:
        json.dump(data, jsonFile)

def save():
    with open('battle_users.json', 'w') as f:
        f.write(json.dumps(data))

@commands.command(name="CreatePlayer", help="Create a player")
async def CreatePlayer(ctx):
    if str(ctx.author.id) not in data:
        data[ctx.author.id] = {
            "name": ctx.author.name,
            "hp": 100,
            "level": 1,
            "exp": 0,
            "gold": 0,
            "attack": 10,
            "defense": 1,
            "speed": 1,
            "items": []
        }
        await ctx.send("Player created!")
        save()
    else:
        await ctx.send("You already have a player!")

def setup(bot):
    bot.add_command(CreatePlayer)