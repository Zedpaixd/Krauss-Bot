import discord
from discord.ext import commands
import random

class util_cog(commands.Cog):

    @commands.command(name="random", help="!!random a b - Provides a random number between a and b")
    async def random(self, ctx, *, query):
        try:
            values = query.strip().split(" ")
            if int(values[0]) > int(values[1]):
                values[0],values[1] = values[1],values[0]
            await ctx.send("A random number between {} and {} is {}".format(values[0],values[1],random.randint(int(values[0]),int(values[1])+1)))
        except:
            await ctx.send("How do you expect me to give you a random integer when you don't input 2 digits")
