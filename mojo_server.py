import discord
from discord.ext import commands
import random
from leakcheck import LeakCheckAPI
import json
import re

token = "OTU2NjE0Njc2NzY5Mjk2NDY0.Yjyy1w.wUua9NIB5exX4P2CPwvUDg9Ar_M"


############### leakcheck API settings ############

api = LeakCheckAPI()
api.set_key("ff6c0c831ddfb396b7a00406965b85869abd3e2c")

####################################################

admin = ['HeAdWi9h#2233']
allowed_users = ['Goblin#9187', 'killzonefury619#8441']

def special_char(pass_string): 
  regex= re.compile('[!#$%^&*+=`\/;\"()<>?\\\|}{~:[\] ]') 
  if(regex.search(pass_string) == None): 
    res = False
  else: 
    res = True
  return(res)

client=commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print('We Ran our CHUTIIYA BOT {0.user}'.format(client))

@client.event
async def on_message(message):
    userid   = message.author.id
    username = str(await client.fetch_user(userid))
    user_msg = str(message.content)

    async def sendfile(response):
            with open("result.txt", "w") as file:
                        file.write(response)
                        file.close()
                
            # send file to Discord in message
            with open("result.txt", "rb") as file:
                await message.channel.send("Your file is:", file=discord.File(file, "result.txt"))
                return

    if(message.author == client.user):
        return

    if(user_msg.lower() == "!sux"):
        response = username
        
        
        await message.channel.send(response)
        return

    if(user_msg.lower().startswith("-l") and (username in (allowed_users + admin) )):
        fill = user_msg.lower().split(" ",1)[1].strip()
        print(fill,"-->",username)
        if(not special_char(fill)):
            if('@' in fill):
                api.set_type("email")
                api.set_query(fill)
                result = api.lookup()
                response = json.dumps(result, sort_keys=True, indent=6)
                pp = response.strip("][")
                if(len(response)>= 1990):
                    await sendfile(response)
                else:
                    pretty_text = "```json"+pp+"```"
                    await message.channel.send(pretty_text)
                    return
            elif('@' not in fill):
                api.set_type("login")
                api.set_query(fill)
                result = api.lookup()
                response = json.dumps(result, sort_keys=True, indent=6)
                pp = response.strip("][")
                if(len(response)>= 1990):
                    await sendfile(response)
                else:
                    pretty_text = "```json"+pp+"```"
                    await message.channel.send(pretty_text)
                    return
        else:
            await message.channel.send("No Valid Arguments Detected")
            return

    if( user_msg.lower().startswith("-allow") and (username in admin) ):

      fill = user_msg.split(" ",1)[1].strip(" <>@!")
      user = str(await client.fetch_user(fill))
      allowed_users.append(user)
      response = user + " Has Been Granted Access !!"
      await message.channel.send(response)

    if( user_msg.lower().startswith("-ban") and (username in admin) ):

      fill = user_msg.split(" ",1)[1].strip(" <>@!")
      user = str(await client.fetch_user(fill))
      allowed_users.remove(user)
      response = user + " Has Been Banned From Sever !!"
      await message.channel.send(response)


        
client.run(token)
