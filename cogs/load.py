import discord
from discord.ext import commands

class Load(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.idle)
        print('Bot ready')

def setup(bot):
    bot.add_cog(Load(bot))