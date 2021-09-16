#pip install discord
#pip install PyNaCl

import discord
from discord.ext import commands
from music_cog import music_cog
from util_cog import util_cog
from economy_cog import *
from game_cog import *
import json


def getPrefix(bot,message):

    try:
        with open ("prefixes.json","r") as file:

            prefixes = json.load(file)
            return prefixes[str(message.guild.id)]

    except KeyError:

        with open("prefixes.json","r") as file:
            prefixes = json.load(file)

        prefixes[str(message.guild.id)] = "!!"


        with open("prefixes.json","w") as file:
            json.dump(prefixes,file)


        with open("prefixes.json","r") as file:
            prefixes = json.load(file)
            return prefixes[str(message.guild.id)]

    except:
        return "!!"

bot = commands.Bot(command_prefix=getPrefix, case_insensitive=True)

bot.add_cog(music_cog(bot))
bot.add_cog(util_cog(bot))
bot.add_cog(econ_cog(bot))
bot.add_cog(game_cog(bot))

with open ("botToken.txt","r") as tkn:
    token = tkn.read()

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Command on cooldown. Please try again in {} seconds".format(int(error.retry_after)))


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

    await ctx.send("Successfully changed the prefix to {}".format(prefix))



@bot.command()
async def ping(ctx):

    await ctx.send('Pong! {} ({} milliseconds)'.format('{0.author.mention}'.format(ctx.message), int(round(bot.latency, 3)*1000)))

bot.run(token)