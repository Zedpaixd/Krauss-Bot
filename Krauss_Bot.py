#pip install discord
#pip install PyNaCl

import discord
from discord.ext import commands
from music_cog import music_cog
from util_cog import util_cog

bot = commands.Bot(command_prefix='!!', case_insensitive=True)

bot.add_cog(music_cog(bot))
bot.add_cog(util_cog(bot))

with open ("botToken.txt","r") as tkn:
    token = tkn.read()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity = discord.Game("!!help"))


bot.run(token)