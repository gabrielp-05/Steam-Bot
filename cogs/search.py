from discord.ext import commands
from utils.get_data import get_data
from utils.load_thread import load_thread
import math
import numpy as np
import logging
import asyncio
import discord

logger = logging.getLogger(__name__)


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='search', aliases=["se"], help="Returns the number of desired results of the given search term(s)")
    async def search(self, ctx, num: int, *, term):
        if isinstance(num, int) and num in range(1, 51):
            await self.bot.change_presence(status=discord.Status.online)

            # replacing spaces with +s so the url can be displayed correctly in Discord
            term = term.replace(' ', '+')

            fetchMessage = await ctx.send('`Fetching data from Steam servers`')
            await asyncio.ensure_future(load_thread(fetchMessage))
            resultsDict = get_data(num, f'https://store.steampowered.com/search/?term={term}&cc=UK')

            await fetchMessage.delete()
            await ctx.send('`Your results are:`')

            messageLineList = list()
            messageLineList.append('`{:<92} {:<15} {:<25} {:<10}`\n'.format(*resultsDict.keys()))

            for row in range(0, len(resultsDict['Products'])):
                messageLineList.append('`{:<92} {:<15} {:<25} {:<10}`\n'.format(resultsDict['Products'][row], resultsDict['Prices'][row], resultsDict['Released'][row], resultsDict['Discounts'][row]))

            noOfMessages = math.ceil(sum(len(line) for line in messageLineList)/2000)

            parts = np.array_split(messageLineList, noOfMessages)
            for part in parts:
                message = ""
                for line in part:
                    message += line
                if len(resultsDict['Products']) > 0:
                    await ctx.send(message)
                else:
                    await ctx.send('`No results were returned`')

            await ctx.send(f'`A link to this can be found at:` **<https://store.steampowered.com/search/?term={term}>**')
            await asyncio.sleep(0.5)
            await self.bot.change_presence(status=discord.Status.idle)
        else:
            await ctx.send('`Please enter a valid number of results to fetch, between 1 and 50`')

def setup(bot):
    bot.add_cog(Search(bot))