import discord
import os
from discord.ext import commands
# import requests
import json
import random
import praw
# from keep_alive import keep_alive
# import datetime
numb=0

client = commands.Bot(command_prefix='papa ')

with open('./gaali.json', 'r'
) as f:  # initializing json file gaali and storing in variable gaali
    gaali = json.load(f)

with open(
        './command.json', 'r'
) as f:  # initializing json file command and storing in variable command
    command = json.load(f)

with open(
        './eightBallResponses.json', 'r'
) as f:  # initializing json file eight ball responses and storing in variable responses
    responses = json.load(f)

with open(
        './roasts.json', 'r'
) as f:  # initializing json file roasts and storing in variable roasts
    roasts = json.load(f)

with open(
        './gaaliResponse.json', 'r'
) as f:  # initializing json file command and storing in variable command
    gaaliResponse = json.load(f)

with open(
        './birthdays.json', 'r'
) as f:  # initializing json file birthdays and storing in variable birthdays
    birthdays = json.load(f)

reddit = praw.Reddit(client_id="9wR8Qu5xnCLMHQ",
                     client_secret=os.getenv("SECRET"),
                     username=os.getenv("USERNAME"),
                     password=os.getenv("PASSWORD"),
                     user_agent="daddy",
                     check_for_async=False)


@client.event
async def on_ready():
    print('logged in as your papa')


@client.command()
async def ping(ctx):
    await ctx.reply('pong')

@client.command()
async def pong(ctx):
  await ctx.reply('ping')
  
@client.command()
async def unga(ctx):
    print('hello')
    await ctx.reply('bunga')

@client.command()
async def bunga(ctx):
  await ctx.reply('pehle unga bol')
  
@client.command()  # papa birthday-vedika-8/10
async def birthday(ctx, *, birthday):
    ls = birthday.split("-")
    name = ls[1]
    month = ls[2].split("/")[1]
    _date = ls[2].split("/")[0]
    birthday[name] = [month, _date]
    await ctx.reply("Birthday added")


@client.command()  # command to add gaali
@commands.has_permissions(administrator=True)
async def add(ctx, *, newgaali):
    if newgaali in gaali:
        await ctx.reply("Gaali exists")
    else:
        gaali.append(newgaali)
        with open('./gaali.json', 'w') as file:
            json.dump(gaali, file)
        await ctx.reply("Gaali added")


@client.command(aliases=['del', 'remove'])  # command to delete gaali
@commands.has_permissions(administrator=True)
async def delete(ctx, *, delgaali):
    gaali.remove(delgaali)
    with open('./gaali.json', 'w') as file:
        json.dump(gaali, file)
        await ctx.reply("Gaali removed")


@client.command()  # display a list of commands
async def commands(ctx):
    await ctx.reply("\n".join(command))


@client.command()  # roast command added
async def roast(ctx, *, person):
    await ctx.send(f"{person} {random.choice(roasts)}")

@client.command(aliases=['sabko bulana']) 
async def sabkobulana(ctx): 
    await ctx.send("@everyone")

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  msl = msg.lower()
  listu = msl.split(' ')

  if len(listu) < 8:
    if " i am" in msg.lower():
        word = msg.split("i am ")[1]
        await message.reply(f"hi {word}, i am papa")

    elif " i'm" in msg.lower():
        word = msg.split("I'm ")[1]
        await message.reply(f"hi {word}, I'm papa")

    elif " im" in msg.lower():
        word = msg.lower().split("im ")[1]
        await message.reply(f"hi {word}, im papa")

    elif msl.startswith("im"):
        word = msg.lower().split("im ")[1]
        await message.reply(f"hi {word}, im papa")

    elif msl.startswith("i'm"):
        word = msg.split("I'm ")[1]
        await message.reply(f"hi {word}, I'm papa")

    elif msl.startswith("i am"):
        word = msg.split("i am ")[1]
        await message.reply(f"hi {word}, i am papa")

  if any(word in gaali for word in listu):
    await message.reply(random.choice(gaaliResponse))

  if "kabootar" in msl:
    await message.channel.send("aao...aao...aao...")

  numb=len(message.mentions)
  for j in range(0,numb):
    if message.mentions[j]==client.user:
      await message.reply("Kya hai?") 

  await client.process_commands(message)


@client.command()
async def meme(ctx):
    subreddit = reddit.subreddit("memes")
    all_subs = []
    hot = subreddit.hot(limit=50)
    for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title=name)

    em.set_image(url=url)
    await ctx.send(embed=em)


@client.command()
async def suno(ctx):
    await ctx.reply(random.choice(responses))
                    

# keep_alive()
client.run('ODMyNjY0MzExMDE2MTk0MDkw.YHnFEQ.kKN5cbP3_EYuksX11zuGKmaw3HY')