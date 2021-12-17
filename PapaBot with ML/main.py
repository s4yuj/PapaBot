import discord
import os
from discord.ext import commands
import requests
import json
import random
import praw

import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import pickle
# from keep_alive import keep_alive
numb=0

client = commands.Bot(command_prefix='papa ')

with open(
          './intent.json', 'r'
          ) as file:
    data = json.load(file)

with open(
          './gaali.json', 'r'
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

reddit = praw.Reddit(client_id="9wR8Qu5xnCLMHQ",
                     client_secret=os.getenv("SECRET"),
                     username=os.getenv("USERNAME"),
                     password=os.getenv("PASSWORD"),
                     user_agent="",
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
  await ctx.reply('bunga')

@client.command()
async def bunga(ctx):
  await ctx.reply('pehle unga bol')


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

# @client.command()
# async def sabkobulana(ctx): 
#     await ctx.send("@everyone")

@client.command(aliases=['sabko bulana'])
async def sabko(ctx):
  if ctx.author.guild_permissions.administrator:
    await ctx.send('@everyone')

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  msl = msg.lower()
  listu = msl.split(' ')

  # if len(listu) < 8:
  #   if " i am" in msg.lower():
  #       word = msg.split("i am ")[1]
  #       await message.reply(f"hi {word}, i am papa")

  #   elif " i'm" in msg.lower():
  #       word = msg.split("I'm ")[1]
  #       await message.reply(f"hi {word}, I'm papa")

  #   elif " im" in msg.lower():
  #       word = msg.lower().split("im ")[1]
  #       await message.reply(f"hi {word}, im papa")

  #   elif msl.startswith("im"):
  #       word = msg.lower().split("im ")[1]
  #       await message.reply(f"hi {word}, im papa")

  #   elif msl.startswith("i'm"):
  #       word = msg.split("I'm ")[1]
  #       await message.reply(f"hi {word}, I'm papa")

  #   elif msl.startswith("i am"):
  #       word = msg.split("i am ")[1]
  #       await message.reply(f"hi {word}, i am papa")



  if any(word in gaali for word in listu):
    await message.reply(random.choice(gaaliResponse))

  if "kabootar" in msl:
    await message.channel.send("aao...aao...aao...")

  numb=len(message.mentions)
  for j in range(0,numb):
    if message.mentions[j]==client.user:
      await message.reply("Kya hai?") 

  await client.process_commands(message)

  model = keras.models.load_model('chat_model')

    # load tokenizer object
  with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
  with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
  max_len = 20
    
  if msg.startswith('$'):
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([msg]),
                                          truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    for i in data['intents']:
        if i['intent'] == tag:
          await message.reply(np.random.choice(i['responses']))


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

# @client.command()
# async def mausam(ctx,*,location):
#     url=f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={os.getenv("APIKEY")}'
#     data=json.loads(requests.get(url).content)
#     await ctx.reply(data)    
                  
client.run("ODMyNjY0MzExMDE2MTk0MDkw.YHnFEQ.kKN5cbP3_EYuksX11zuGKmaw3HY")

# @client.command()
# async def papa():
#     # load trained model
#     model = keras.models.load_model('chat_model')

#     # load tokenizer object
#     with open('tokenizer.pickle', 'rb') as handle:
#         tokenizer = pickle.load(handle)

#     # load label encoder object
#     with open('label_encoder.pickle', 'rb') as enc:
#         lbl_encoder = pickle.load(enc)

#     # parameters
#     max_len = 20
    
#     while True:
#         inp = input()
#         if inp.lower() == "quit":
#             break

#         result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
#                                              truncating='post', maxlen=max_len))
#         tag = lbl_encoder.inverse_transform([np.argmax(result)])

#         for i in data['intents']:
#             if i['intent'] == tag:
#                 print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , np.random.choice(i['responses']))
