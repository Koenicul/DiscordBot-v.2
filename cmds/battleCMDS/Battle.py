from discord.ext import commands
import json
import discord

data = {}
current_battle = {}
game_over = True
turn = 0
base_health = 100
p1_move_made = False
p2_move_made = False
winner = 0
attackTypes = {}

def check_winner(p1, p2):
    global game_over
    
    if p1['hp'] <= 0:
        game_over = True
        return 2
    elif p2['hp'] <= 0:
        game_over = True
        return 1
    else:
        return 0

async def Fwinner(ctx, p1, p2):
    print(p1)
    print(p2)
    await ctx.send(f'{p1["name"]} wins!')

@commands.command(name="Battle", help="Start a battle")
async def Battle(ctx, user2: discord.Member):
    try:
        with open('battle_users.json', 'r') as f:
            data = json.load(f)
    except:
        with open('battle_users.json', 'w') as jsonFile:
            json.dump(data, jsonFile)

    global game_over
    
    user1 = ctx.message.author
    if game_over:
        if user1.id != user2.id:
            try:
                player_1 = data[str(user1.id)]
            except:
                await ctx.send(f"{user1.display_name} has not created a player!")
                return
            
            try:
                player_2 = data[str(user2.id)]
            except:
                await ctx.send(f"{user2.display_name} has not created a player!")
                return

            p1 = data[str(user1.id)]
            p2 = data[str(user2.id)]
            
            if p1['speed'] > p2['speed']:
                current_battle[user1.id] = []
                current_battle[user2.id] = []
            else:
                current_battle[user2.id] = []
                current_battle[user1.id] = []

            await ctx.send(f"{user1.mention} has started a battle with {user2.mention}")

            game_over = False
        else:
            await ctx.send("You can't battle yourself!")
    else:
        await ctx.send("A battle is already in progress!")

def check_move(p1, p2, attackType): 
    if p1 == ['attack'] and p2 != ['block'] and attackType == [1]:
        return 1
    elif p1 == ['attack'] and p2 == ['block'] and attackType == [1]:
        return 2
    elif p1 == ['attack'] and p2 != ['block'] and attackType == [2]:
        return 7
    elif p1 == ['attack'] and p2 == ['block'] and attackType == [2]:
        return 8
    elif p1 == ['item']:
        return 3
    elif p1 == ['surrender'] and p2 != ['surrender']:
        return 4
    elif p1 == ['block'] and p2 == ['block']:
        return 5
    elif p1 == ['surrender'] and p2 == ['surrender']:
        return 6 

@commands.command(name="Move", help="Move in battle")
async def Move(ctx, option: int, attackType = 0):
    pass

@Battle.error
async def Battle_error(ctx):
    await ctx.send("Please make sure to mention a player.")

def setup(bot):
    bot.add_command(Battle)
    bot.add_command(Move)