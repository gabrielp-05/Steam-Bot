import discord
from discord.ext import commands

class OnCommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            return
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send('**Please pass in all required arguments**')

def setup(bot):
    bot.add_cog(OnCommandError(bot))