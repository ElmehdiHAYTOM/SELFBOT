import discord
import discord,asyncio,youtube_dl
import os
from discord.ext import commands,tasks
from dotenv import load_dotenv
###################################################################
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return "server online!"

def run():
    app.run(host="0.0.0.0", port=8080)
    
def keep_alive():
    server = Thread(target=run)
    server.start()


###################################################################
load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="HB!",intents=intents,self_bot=1)


cogs=["AFK","Cloner","Profile","Spy","Music"]

@bot.event
async def on_ready():
    
            
    for i in cogs:
        bot.load_extension("cogs."+i)
    print(bot.user.name)



while __name__ == '__main__':
  try:
    keep_alive()
    bot.run(os.environ["TOKEN"],bot=0)
  except discord.errors.HTTPException as e:
    print(e)
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system('kill 1')