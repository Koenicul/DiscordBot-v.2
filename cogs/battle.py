from discord.ext import commands
import discord
from cmds.battle.create_player import create_player
from cmds.battle.shop import shop, buy
from cmds.battle.inventory import inventory, equip, unequip
from cmds.battle.daily import daily, convert
from cmds.battle.battle import battle, move

class Battle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="CreatePlayer", help="Creates a player")
    async def CreatePlayer(self, ctx):
        await create_player(ctx)

    @commands.command(name="Shop", help="Opens the shop")
    async def Shop(self, ctx):
        await shop(ctx)

    @commands.command(name="Buy", help="Buys an item")
    async def Buy(self, ctx, index: int):
        await buy(ctx, index)

    @commands.command(name="Inventory", help="Opens the inventory")
    async def Inventory(self, ctx):
        await inventory(ctx)

    @commands.command(name="Equip", help="Equips an item")
    async def Equip(self, ctx, item: int):
        await equip(ctx, item)

    @commands.command(name="Unequip", help="Unequips an item")
    async def Unequip(self, ctx, item):
        await unequip(ctx, item)

    @commands.command(name="Daily", help="Get your daily reward")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def Daily(self, ctx):
        await daily(ctx)

    @commands.command(name="Battle", help="Start a battle")
    async def Battle(self, ctx, user2: discord.Member):
        await battle(ctx, user2)

    @commands.command(name="Move", help="Move in a battle")
    async def Move(self, ctx, option: int, attackType = 0):
        await move(ctx, option, attackType)
    
    @Daily.error
    async def command_name_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            time = convert(error.retry_after)
            embed = discord.Embed(title=f"You are in cooldown",description=f"Try again in {time}.", color=discord.Color.orange())
            await ctx.send(embed=embed)

    @Battle.error
    async def Battle_error(ctx):
        await ctx.send("Please make sure to mention a player.")

def setup(bot):
    bot.add_cog(Battle(bot))