#pip install discord
#pip install PyNaCl

import discord
from discord.ext import commands
from music_cog import music_cog
from util_cog import util_cog
from economy_cog import *
import json

def getPrefix(bot,message):

    with open ("prefixes.json","r") as file:

        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=getPrefix, case_insensitive=True)

bot.add_cog(music_cog(bot))
bot.add_cog(util_cog(bot))
bot.add_cog(econ_cog(bot))

with open ("botToken.txt","r") as tkn:
    token = tkn.read()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity = discord.Game("!!help"))


@bot.event
async def on_guild_join(guild):

    with open("prefixes.json","r") as file:

        prefixes = json.load(file)

    prefixes[str(guild.id)] = "!!"

    with open("prefixes.json","w") as file:

        json.dump(prefixes,file)



@bot.command(name = "setPrefix", help="setPrefix x - Sets the bot prefix to x")
async def setPrefix(ctx,prefix):

    with open("prefixes.json","r") as file:

        prefixes = json.load(file)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json","w") as file:

        json.dump(prefixes,file)


bot.run(token)