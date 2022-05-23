from discord.ext import commands

class Start(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is online.')
    
def setup(bot):
    bot.add_cog(Start(bot))