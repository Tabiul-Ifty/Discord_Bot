import os
import discord 
import requests
import random
import json
from replit import db
from keep_alive import keep_alive



client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "vallagena",
"kosto", "koste asi", "kosto", "vala na", "bal"]

starter_encouragement = [
  "cheer up!", 
  "hang in there", 
  "you are grate!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_qoute():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  qoute = json_data[0]['q'] + " -- " + json_data[0]['a']
  return(qoute)

def get_joke():
  response = requests.get("https://official-joke-api.appspot.com/random_joke")
  json_data = json.loads(response.text)
  joke = json_data['setup'] + '\n' + json_data['punchline']
  return(joke)

def get_insult():
  response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
  json_data = json.loads(response.text)
  insult = json_data['insult']
  return(insult)

def get_meme():
  response = requests.get("https://meme-api.herokuapp.com/gimme/marvelmemes")
  json_data = json.loads(response.text)
  meme = json_data['url']
  return(meme)


def update_encouragement(encouraging_message):
  if "encouragement" in db.keys():
    encouragement = db["encouragement"]
    encouragement.append(encouraging_message)
    db["encouragement"] = encouragement
  else:
    db["encouragement"] = [encouraging_message]


def delete_encouragement(index):
  encouragement = db["encouragement"]
  if len(encouragement)>index:
    del encouragement[index]
    db["encouragement"] = encouragement


@client.event
async def on_ready():
  print('we are logged in as {0.user}'
  .format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("$joke"):
    joke = get_joke()
    await message.channel.send(joke)
 
  if msg.startswith('$inspire'):
    qoute = get_qoute()
    await message.channel.send(qoute)

  if msg.startswith('$insult'):
    insult = get_insult()
    await message.channel.send(insult)

  if msg.startswith('$meme'):
    meme = get_meme()
    await message.channel.send(meme)


  if db["responding"]:
    options = starter_encouragement
    if "encouragement" in db.keys():
      # options = options + db["encouragement"]
      options = options + list(db["encouragement"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

    # if any(word in msg for word in sad_words):
    #   await message.channel.send(random.choice(starter_encouragement))

  if msg.startswith("$new"):
    encouraging_message =  msg.split("$new ",1)[1]
    update_encouragement(encouraging_message)
    await message.channel.send("New encouraging_message added")


  if msg.startswith("$del"): 
    encouragement = []
    if "encouragement" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragement = db["encouragement"]
    await message.channel.send(encouragement)

  if msg.startswith("$list"):
    encouragement = []
    if "encouragement" in db.keys():
      encouragement = db["encouragement"]
    await message.channel.send(encouragement)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == 'true':
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is Off.")
    

    


my_secret = os.environ['TOKEN']
keep_alive()
client.run(my_secret)







