from discord.ext import commands
import discord

class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            embed = discord.Embed(title=f"Welcome!", description=f"Hello {member.mention}, make sure to read the rules!", color=0x00ff00)
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Start(bot))