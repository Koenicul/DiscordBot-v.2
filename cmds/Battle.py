from discord.ext import commands
import json

data = {}
base = 500

try:
    with open('battle_users.json', 'r') as f:
        data = json.load(f)
except:
    with open('battle_users.json', 'w') as jsonFile:
        json.dump(data, jsonFile)

def save():
    with open('battle_users.json', 'w') as f:
        f.write(json.dumps(data))

@commands.command(name="Battle", help="Start a battle")
async def Battle(ctx, user2=""):
    if user2 != "":
        user1 = ctx.message.author.name
        if not user1 in data:
            data[user1] = []
            data[user1].append(base)
        else:
           print(f"{user1} is already in database")

        if not user2 in data:
            data[user2] = []
            data[user2].append(base)
        else:
            print(f"{user2} is already in database")
    else:
        await ctx.send("Enter opponent!")
    
    save()

def setup(bot):
    bot.add_command(Battle)