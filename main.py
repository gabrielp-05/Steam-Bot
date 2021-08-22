from discord.ext import commands
from discord import Intents

import numpy as np
from bs4 import BeautifulSoup
from keep_alive import keep_alive
import discord, os, asyncio, requests, math

#---------------------------------------------------------#
# web scraper

def scraper(num, page) -> dict:

  """
  When a valid URL is passed in, it opens that page in the Selenium Chromedriver and
  fetches all results in a given range which can be changed
  """

  products = []
  releases = []
  discounts = []
  prices = []

  content = requests.get(page, 'html.parser')
  soup = BeautifulSoup(content.text, features="html.parser")

  for a in soup.findAll('a', attrs = {'class': 'search_result_row'}):
    name = a.find('span', attrs={'class': 'title'})
    price = a.find('div', attrs={'class': 'search_price'})
    discount = a.find('div', attrs={'class': 'search_discount'})
    release = a.find('div', attrs={'class': 'search_released'})

    products.append(name.text.strip())
    releases.append(release.text.strip())

    try:
      prices.append(price.contents[3].strip())
    except Exception:
      prices.append(price.contents[0].strip())

    discounts.append(discount.text.strip())

    if len(prices) == num:
      break

  resultsDict = {'Products':products, 'Prices':prices, 'Releases':releases, 'Discounts':discounts}
  return resultsDict


# bot

client = commands.Bot(command_prefix='>', intents = Intents.all(), help_command=None)

statusName = 'The best bot.'

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.idle)
  print('Bot ready')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send('**Please pass in all required arguments**')

async def load_thread(fetchMessage):
  msg = 'Fetching data from Steam servers'
  await fetchMessage.edit(content=msg+'.')
  await asyncio.sleep(0.5)
  await fetchMessage.edit(content=msg+'..')
  await asyncio.sleep(0.5)
  await fetchMessage.edit(content=msg+'...')
  await asyncio.sleep(0.5)



@client.command(name='help')
async def help(ctx):
    em = discord.Embed(title='Help', description='A bot that can be used to pull results and sales off the Steam webstore.', colour=discord.Color.dark_blue())
    em.add_field(name='Sales', value='Allows the user to be returned the sales page from Steam. Syntax: >sales [no. of results]; leave [no. of results] empty to be returned 20 by default')
    em.add_field(name='Search', value='Allows the user to search for results on Steam. Syntax: >search [no. of results] [search term]')
    await ctx.send(embed = em)


# fetch sales
@client.command(name='sales')
async def sales(ctx, num : int = 20):

  if isinstance(num, int) and num in range(1,26):
    await client.change_presence(status=discord.Status.online)
    fetchMessage = await ctx.send('Fetching data from Steam servers...')
    await asyncio.ensure_future(load_thread(fetchMessage))
    resultsDict = scraper(num, 'https://store.steampowered.com/search/?specials=1/&cc=UK')
    
    await fetchMessage.delete()
    await ctx.send('The latest sales on Steam are:')
    
    messageLineList = list()
    messageLineList.append('`{:<90} {:<15} {:<25} {:<10}`\n'.format(*resultsDict.keys()))

    for row in range(0,len(resultsDict['Products'])):
      messageLineList.append('`{:<90} {:<15} {:<25} {:<10}`\n'.format(resultsDict['Products'][row], resultsDict['Prices'][row], resultsDict['Releases'][row], resultsDict['Discounts'][row]))

    noOfMessages = math.ceil(sum(len(line) for line in messageLineList)/2000)

    parts = np.array_split(messageLineList,noOfMessages)
    for part in parts:
      message = ""
      for line in part:
        message += line
      if len(resultsDict['Products']) > 0: await ctx.send(message)
      else: await ctx.send('`**No results were returned**`')

    await ctx.send('A link to this can be found at <https://bit.ly/3k8rqS0>')
    await asyncio.sleep(0.5)
    await client.change_presence(status=discord.Status.idle)
  else:
    await ctx.send('Please enter a valid number of results to fetch, between 1 and 25')


# search
@client.command(name='search')
async def search(ctx, num : int, *, term):

  if isinstance(num, int) and num in range(1,26):
    await client.change_presence(status=discord.Status.online)

    term = term.replace(' ','+') # replacing spaces with +s so the url can be displayed correctly in Discord

    fetchMessage = await ctx.send('Fetching data from Steam servers...')
    await asyncio.ensure_future(load_thread(fetchMessage))
    resultsDict = scraper(num, f'https://store.steampowered.com/search/?term={term}&cc=UK')

    await fetchMessage.delete()
    await ctx.send('Your results are:')

    messageLineList = list()
    messageLineList.append('`{:<90} {:<15} {:<25} {:<10}`\n'.format(*resultsDict.keys()))

    for row in range(0,len(resultsDict['Products'])):
      messageLineList.append('`{:<90} {:<15} {:<25} {:<10}`\n'.format(resultsDict['Products'][row], resultsDict['Prices'][row], resultsDict['Releases'][row], resultsDict['Discounts'][row]))

    noOfMessages = math.ceil(sum(len(line) for line in messageLineList)/2000)

    parts = np.array_split(messageLineList,noOfMessages)
    for part in parts:
      message = ""
      for line in part:
        message += line
      if len(resultsDict['Products']) > 0: await ctx.send(message)
      else: await ctx.send('`**No results were returned**`')

    await ctx.send(f'A link to this can be found at <https://store.steampowered.com/search/?term={term}>')
    await asyncio.sleep(0.5)
    await client.change_presence(status=discord.Status.idle)
  else:
    await ctx.send('Please enter a valid number of results to fetch, between 1 and 25')

keep_alive()
token = os.environ.get('Token') # if copying this code, make sure to have an environment file with a variable named 'Token' with the bot's oauth token as the value in order for it to run.
client.run(token)
