from discord.ext import commands
import json
import discord

data = {}
items = {}
current_battle = {}
game_over = True
turn = 0
base_health = 100
p1_move_made = False
p2_move_made = False
winner = 0
attackTypes = {}
potions = {}

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
    p1['hp'] = p1['maxhp']
    p2['hp'] = p2['maxhp']
    current_battle.clear()
    with open('battle_users.json', 'w') as f:
        f.write(json.dumps(data))
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
    global winner
    
    user1 = ctx.message.author
    if game_over:
        if user1.id != user2.id:
            try:
                data[str(user1.id)]
            except:
                await ctx.send(f"{user1.display_name} has not created a player!")
                return
            
            try:
                data[str(user2.id)]
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

            await ctx.send(f"{user2.mention} do you accept to battle {user1.mention}? (yes/no)")
            msg = await ctx.bot.wait_for('message', check=lambda message: message.author == user2)
            if msg.content.lower() == 'yes':
                await ctx.send(f"{user1.mention} has started a battle with {user2.mention}")
                winner = 0
                game_over = False
            elif msg.content.lower() == 'no':
                await ctx.send(f"{user2.mention} didn't accept the battle!")
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
    elif 'item' in p1:
        return 3
    elif p1 == ['surrender'] and p2 != ['surrender']:
        return 4
    elif p1 == ['block'] and p2 == ['block']:
        return 5
    elif p1 == ['surrender'] and p2 == ['surrender']:
        return 6
    elif p1 == ['block'] and p2 != ['attack']:
        return 9

@commands.command(name="Move", help="Move in battle")
async def Move(ctx, option: int, attackType = 0):
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
                    usedItem = await useItem(ctx, p1)
                    if usedItem != 0:
                        current_battle[ctx.author.id] = ['item']
                        current_battle[ctx.author.id].append(usedItem)
                    else:
                        return
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
                    usedItem = await useItem(ctx, p2)
                    if usedItem != 0:
                        current_battle[ctx.author.id] = ['item']
                        current_battle[ctx.author.id].append(usedItem)
                    else:
                        return
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
                        if player_1['hp'] + items[current_battle[player][1]]['effect'] > player_1['maxhp']:
                            player_1['hp'] = player_1['maxhp']
                        else:
                            player_1['hp'] += items[current_battle[player][1]]['effect']
                        
                        potions.clear()
                        player_1['items'].remove(current_battle[player][1])
                        await ctx.send(f"{player_1['name']} used {items[current_battle[player][1]]['name']} and recovered {items[current_battle[player][1]]['effect']} HP!")
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
                    if move_case == 9:
                        await ctx.send(f"{player_1['name']} blocked but {player_2['name']} didn't attack!")

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

        else:
            await ctx.send("Invalid option!")
        with open('battle_users.json', 'w') as f:
            f.write(json.dumps(data))
    else:
        await ctx.send("No game has started.")

async def useItem(ctx, player):
    try:
        with open('items.json', 'r') as f:
            items = json.load(f)
    except:
        with open('items.json', 'w') as jsonFile:
            json.dump(items, jsonFile)

    index = 1

    for i in player["items"]:
        if items[i]["effectType"] == "potion":
            potions[index] = items[i]
            potions[index]["item"] = i

            index += 1
    
    if len(potions) > 0:
        await ctx.send(f"potions: " + ", ".join(potions[i]["name"] for i in potions) + ".")

        msg = await ctx.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        try:
            if 0 < int(msg.content) <= len(potions):
                return potions[int(msg.content)]['item']
            else:
                await ctx.send("Invalid number")
                return 0
        except:
            await ctx.send("Enter a number")
            return 0
    else:
        await ctx.send("You have no items")
        return 0

@Battle.error
async def Battle_error(ctx):
    await ctx.send("Please make sure to mention a player.")

def setup(bot):
    bot.add_command(Battle)
    bot.add_command(Move)