from discord.ext import commands
from utils.get_data import get_data
from utils.load_thread import load_thread
import math
import numpy as np
import logging
import asyncio
import discord

logger = logging.getLogger(__name__)


class Sales(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sales', aliases=["sa"], help="Returns the number of desired results of top sales on the Steam Store")
    async def sales(self, ctx, num: int = 20):

        if isinstance(num, int) and num in range(1, 51):
            await self.bot.change_presence(status=discord.Status.online)
            fetchMessage = await ctx.send('`Fetching data from Steam servers`')
            await asyncio.ensure_future(load_thread(fetchMessage))
            try:
                resultsDict = get_data(num, 'https://store.steampowered.com/search/?specials=1/&cc=UK')
            except Exception as e:
                logging.error(e)
                return await ctx.send("**There was an error fetching the data**")
            await fetchMessage.delete()
            await ctx.send('`The latest sales on Steam are:`')

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

            await ctx.send('`A link to this can be found at:` **<https://bit.ly/3k8rqS0>**')
            await asyncio.sleep(0.5)
            await self.bot.change_presence(status=discord.Status.idle)
        else:
            await ctx.send('`Please enter a valid number of results to fetch, between 1 and 50`')

def setup(bot):
    bot.add_cog(Sales(bot))