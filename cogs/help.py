from discord.ext import commands
import logging
import discord

logger = logging.getLogger(__name__)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=["h"])
    async def help(self, ctx):
        em = discord.Embed(title='Help', description='A bot that can be used to pull results and sales off the Steam webstore.', colour=discord.Color.dark_blue())
        em.add_field(name='Sales', value='Allows the user to be returned the sales page from Steam. Syntax: >sales [no. of results]; leave [no. of results] empty to be returned 20 by default', inline=False)
        em.add_field(name='Search', value='Allows the user to search for results on Steam. Syntax: >search [no. of results] [search term]', inline=False)
        await ctx.send(embed = em)

def setup(bot):
    bot.add_cog(Help(bot))