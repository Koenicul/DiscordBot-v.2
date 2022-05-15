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
    try:
        with open('battle_users.json', 'r') as f:
            data = json.load(f)
    except:
        with open('battle_users.json', 'w') as jsonFile:
            json.dump(data, jsonFile)

    global game_over
    global turn
    global p1_move_made
    global p2_move_made
    global winner

    if not game_over:
        if 0 < option < 5:
            p1 = data[str(list(current_battle.keys())[0])]
            p2 = data[str(list(current_battle.keys())[1])]

            if list(current_battle.keys())[0] == ctx.author.id and not p1_move_made:
                attackTypes[ctx.author.id] = [attackType]

                if option == 1:
                    current_battle[ctx.author.id] = ['attack']
                elif option == 2:
                    current_battle[ctx.author.id] = ['block']
                elif option == 3:
                    current_battle[ctx.author.id] = ['item']
                else:
                    current_battle[ctx.author.id] = ['surrender']
                p1_move_made = True
            elif list(current_battle.keys())[1] == ctx.author.id and not p2_move_made:
                attackTypes[ctx.author.id] = [attackType]

                if option == 1:
                    current_battle[ctx.author.id] = ['attack']
                elif option == 2:
                    current_battle[ctx.author.id] = ['block']
                elif option == 3:
                    current_battle[ctx.author.id] = ['item']
                else:
                    current_battle[ctx.author.id] = ['surrender']
                p2_move_made = True

            if p1_move_made and p2_move_made:
                i = 1
                for player in current_battle:
                    player_1 = data[str(player)]
                    player_2 = data[str(list(current_battle.keys())[i])]
                    cur_attackType = attackTypes[player]

                    move_case = check_move(current_battle[player], current_battle[list(current_battle.keys())[i]], cur_attackType)
                    if move_case == 1:
                        player_2['hp'] -= player_1['attack'] * player_2['defense']
                        await ctx.send(f"{player_1['name']} light attacked {player_2['name']} for {player_1['attack'] * player_2['defense']} damage!")
                    if move_case == 2:
                        await ctx.send(f"{player_2['name']} blocked {player_1['name']}'s attack!")
                    if move_case == 3:
                        await ctx.send(f"{player_1['name']} used an item!")
                    if move_case == 4:
                        await ctx.send(f"{player_1['name']} surrendered!")
                        await Fwinner(ctx, player_2, player_1)
                        game_over = True
                    if move_case == 5:
                        await ctx.send("Both players blocked!")
                        break
                    if move_case == 6:
                        await ctx.send("Both players surrendered!")
                        game_over = True
                        break
                    if move_case == 7:
                        player_2['hp'] -= player_1['attack'] * player_2['defense'] * 0.5
                        await ctx.send(f"{player_1['name']} heavy attacked {player_2['name']} for {player_1['attack'] * player_2['defense'] * 0.5} damage!")
                    if move_case == 8:
                        player_2['hp'] -= player_1['attack'] * player_2['defense'] * 1.5
                        await ctx.send(f"{player_1['name']} heavy attacked {player_2['name']} for {player_1['attack'] * player_2['defense'] * 1.5} damage!")

                    winner = check_winner(p1, p2)

                    if winner != 0:
                        break
                    
                    i -= 1
                p1_move_made = False
                p2_move_made = False

            if winner == 1:
                await Fwinner(ctx, p1, p2)
            
            if winner == 2:
                await Fwinner(ctx, p2, p1)
            
            if game_over:
                p1['hp'] = base_health
                p2['hp'] = base_health
                with open('battle_users.json', 'w') as f:
                    f.write(json.dumps(data))

        else:
            await ctx.send("Invalid option!")
        with open('battle_users.json', 'w') as f:
            f.write(json.dumps(data))
    else:
        await ctx.send("No game has started.")

@Battle.error
async def Battle_error(ctx):
    await ctx.send("Please make sure to mention a player.")

def setup(bot):
    bot.add_command(Battle)
    bot.add_command(Move)