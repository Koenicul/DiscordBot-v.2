from discord.ext import commands
import discord
from sqlalchemy.orm import sessionmaker
import db

Session = sessionmaker(bind=db.engine)
session = Session()

current_battle = {}
game_over = True
turn = 0
base_health = 100
p1_move_made = False
p2_move_made = False
winner = 0
attackTypes = {}
potions = {}
channel = None

reward_lookup = {
    tuple(range(101, 10000)): 70,
    tuple(range(90, 100)): 65,
    tuple(range(80, 89)): 63,
    tuple(range(70, 79)): 60,
    tuple(range(60, 69)): 57,
    tuple(range(50, 59)): 54,
    tuple(range(40, 49)): 50,
    tuple(range(30, 39)): 45,
    tuple(range(20, 29)): 49,
    tuple(range(10, 19)): 32,
    tuple(range(0, 9)): 25,
    tuple(range(-9, 0)): 25,
    tuple(range(-19, -10)): 24,
    tuple(range(-29, -20)): 23,
    tuple(range(-39, -30)): 21,
    tuple(range(-49, -40)): 19,
    tuple(range(-59, -50)): 16,
    tuple(range(-69, -60)): 13,
    tuple(range(-79, -70)): 10,
    tuple(range(-89, -80)): 8,
    tuple(range(-100, -90)): 6,
    tuple(range(-10000, -101)): 5
}

def check_winner(p1, p2):
    global game_over
    
    if p1.hp <= 0:
        game_over = True
        return 2
    elif p2.hp <= 0:
        game_over = True
        return 1
    else:
        return 0

async def Fwinner(p1, p2):
    global channel
    embed = discord.Embed(title="Battle Over!", description=f"{p1.name} has won the battle!", color=0x00ff00)

    p1.hp = p1.maxhp
    p2.hp = p2.maxhp

    change = calcReward(p1, p2)

    embed.add_field(name=f"{p1.name} reward:", value=f"{int(change / 2)} exp\n{change} gold")
    embed.add_field(name=f"{p2.name} reward:", value=f"{int(change / 10)} exp\n{int(change / 10)} gold")

    p1.exp += int(change / 2)
    p1.gold += change
    await checkExp(p1)

    p2.exp += int(change / 10)
    p2.gold += int(change / 10)
    await checkExp(p2)

    await channel.send(embed=embed)


def calcReward(p1, p2):
    diff = p2.level - p1.level
    for key in reward_lookup:
        if diff in key:
            return reward_lookup[key]

async def checkExp(player):
    global channel
    if player.exp >= player.level * 10:
        player.maxhp += 10
        player.hp += 10
        player.exp -= player.level * 10
        player.level += 1

        session.commit()

        embed = discord.Embed(title="Level Up!", description=f"{player.name} has leveled up to level {player.level}!", color=0x00ff00)
        embed.add_field(name="Health has increased by 10!", value=f"{player.name} now has {player.maxhp} health!")
        embed.add_field(name=f"{player.name} now needs:", value=f"{player.level * 10 - player.exp} exp to level up!")

        await channel.send(embed=embed)

@commands.command(name="Battle", help="Start a battle")
async def Battle(ctx, user2: discord.Member):
    global game_over
    global winner
    global channel

    player_1 = session.query(db.Player).filter_by(id=ctx.author.id).first()
    player_2 = session.query(db.Player).filter_by(id=user2.id).first()

    user1 = ctx.message.author

    if game_over:
        if user1.id != user2.id:
            if player_1 is None:
                embed = discord.Embed(
                    title=f"{user1.display_name} doesn't have a player yet!",
                    description='Do you want to create a player?'
                )
                return await ctx.send(embed=embed)
            if player_2 is None:
                embed = discord.Embed(
                    title=f"{user2.display_name} doesn't have a player yet!",
                    description='Do you want to create a player?'
                )
                return await ctx.send(embed=embed)

            embed = discord.Embed(
                title=f"{user1.display_name} vs {user2.display_name}",
                description=f"{user2.mention} do you want to battle {user1.mention}? (yes/no)",
            )
            await ctx.send(embed=embed)
            msg = await ctx.bot.wait_for('message', check=lambda message: message.author == user2)
            if msg.content.lower() == 'yes':
                
                current_battle.clear()
                channel = None

                if player_1.speed > player_2.speed:
                    current_battle[player_1.id] = []
                    current_battle[player_2.id] = []
                else:
                    current_battle[player_2.id] = []
                    current_battle[player_1.id] = []

                embed = discord.Embed(title="A battle has started!", description=f"{user1.mention} VS {user2.mention}")
                await ctx.send(embed=embed)

                embed = discord.Embed(
                    title="Move:",
                    description="Choose your move: (attack/block/item/surrender)",
                )

                embed.set_footer(text="Type '--move <move index>' to make your move!")

                await user1.send(embed=embed)
                await user2.send(embed=embed)

                channel = ctx.bot.get_channel(ctx.channel.id)
                winner = 0
                game_over = False
                player_1.hp = player_1.maxhp
                player_2.hp = player_2.maxhp

            else:
                embed = discord.Embed(title=f"{user2.display_name} has declined the battle")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You can't battle yourself!")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"There is already a battle going on!")
        await ctx.send(embed=embed)

    session.commit()

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
    global game_over
    global turn
    global p1_move_made
    global p2_move_made
    global winner
    global channel

    if not game_over:
        if 0 < option < 5:
            p1 = session.query(db.Player).filter(db.Player.id == list(current_battle.keys())[0]).first()
            p2 = session.query(db.Player).filter(db.Player.id == list(current_battle.keys())[1]).first()

            if ctx.author.id == p1.id and not p1_move_made:
                attackTypes[ctx.author.id] = [attackType]

                if option == 1:
                    if attackType != 0:
                        current_battle[ctx.author.id] = ['attack']
                    else:
                        return
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

            elif ctx.author.id == p2.id and not p2_move_made:
                attackTypes[ctx.author.id] = [attackType]

                if option == 1:
                    if attackType != 0:
                        current_battle[ctx.author.id] = ['attack']
                    else:
                        return
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
                embed = discord.Embed(
                    title="Battle", 
                    color=0x00ff00
                )
                for player in current_battle:
                    player_1 = session.query(db.Player).filter(db.Player.id == player).first()
                    player_2 = session.query(db.Player).filter(db.Player.id == (list(current_battle.keys())[i])).first()
                    cur_attackType = attackTypes[player]

                    move_case = check_move(current_battle[player], current_battle[list(current_battle.keys())[i]], cur_attackType)

                    if move_case == 1:
                        player_2.hp -= player_1.attack * player_2.defense
                        embed.add_field(name=f"{player_1.name} light attacked {player_2.name} for {player_1.attack * player_2.defense} damage!", value="test")
                    if move_case == 2:
                        player_1.hp -= player_1.attack * player_1.defense * 0.5
                        embed.add_field(name=f"{player_2.name} blocked {player_1.name}'s attack!", value="test")
                    if move_case == 3:
                        item = session.query(db.PlayerItem).filter(db.PlayerItem.id == current_battle[player][1]).first()
                        if player_1.hp + item.item.effect > player_1.maxhp:
                            player_1.hp = player_1.maxhp
                        else:
                            player_1.hp += item.item.effect
                        
                        potions.clear()
                        session.query(db.PlayerItem).filter(db.PlayerItem.id==item.id).delete()
                        embed.add_field(name=f"{player_1.name} used {item.item.name} and recovered {item.item.effect} HP!", value="test")
                        print("check")
                    if move_case == 4:
                        embed.add_field(name=f"{player_1.name} surrendered!", value="test")
                        await Fwinner(player_2, player_1)
                        game_over = True
                    if move_case == 5:
                        embed.add_field(name="Both players blocked!", value="test")
                    if move_case == 6:
                        embed.add_field(name="Both players surrendered!", value="test")
                        game_over = True
                        break
                    if move_case == 7:
                        player_2.hp -= player_1.attack * player_2.defense * 0.5
                        embed.add_field(name=f"{player_1.name} heavy attacked {player_2.name} for {player_1.attack * player_2.defense * 0.5} damage!", value="test")
                    if move_case == 8:
                        player_2.hp -= player_1.attack * player_2.defense * 1.5
                        embed.add_field(name=f"{player_1.name} heavy attacked {player_2.name} for {player_1.attack * player_2.defense * 1.5} damage!", value="test")
                    if move_case == 9:
                        embed.add_field(name=f"{player_1.name} blocked but {player_2.name} didn't attack!", value="test")

                    winner = check_winner(p1, p2)
                    
                    i -= 1

                await channel.send(
                    f"<@{list(current_battle.keys())[0]}> vs <@{list(current_battle.keys())[1]}>",
                    embed=embed
                )

                p1_move_made = False
                p2_move_made = False
                if not game_over:
                    p1_user = await ctx.bot.fetch_user(str(list(current_battle.keys())[0]))
                    p2_user = await ctx.bot.fetch_user(str(list(current_battle.keys())[1]))

                    embed = discord.Embed(
                        title="Move:",
                        description="Choose your move: (attack/block/item/surrender)",
                    )

                embed.set_footer(text="Type '--move <move index>' to make your move!")

                await p1_user.send(embed=embed)
                await p2_user.send(embed=embed)

            if winner == 1:
                await Fwinner(p1, p2)
            
            if winner == 2:
                await Fwinner(p2, p1)

        else:
            await ctx.send("Invalid option!")
    else:
        await ctx.send("No game has started.")

    session.commit()

async def useItem(ctx, player):
    index = 1
    embed = discord.Embed(title="Potions:", description="Choose your potion:")
    embed.set_footer(text="Type '<potion index>' to use your potion!")
    for item in player.playerItems:
        if item.item.type == "potion":
            potions[index] = item.id
            embed.add_field(name=f"{index}: {item.item.name}", value=f"{item.item.effect} HP")

            index += 1
    
    if len(potions) > 0:
        await ctx.send(embed=embed)

        msg = await ctx.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        try:
            if 0 < int(msg.content) <= len(potions):
                return potions[int(msg.content)]
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