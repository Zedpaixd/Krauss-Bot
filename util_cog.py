import discord
from discord.ext import commands
import random
import json 

# PING - PONG (delay + tag author)
# !!kill - Killing is bad.

class util_cog(commands.Cog):

    @commands.command(name="random", help="random a b - Provides a random number between a and b")
    async def random(self, ctx, *, query):

        try:
            values = query.strip().split(" ")

            if int(values[0]) > int(values[1]):
                values[0],values[1] = values[1],values[0]

            await ctx.send("A random number between {} and {} is {}".format(values[0],values[1],random.randint(int(values[0]),int(values[1])+1)))
        
        except:
            await ctx.send("How do you expect me to give you a random integer when you don't input 2 digits")



    @commands.command(name="bully", help="bully @Person - You virtually bully a person in a unique way")
    async def bully(self, ctx, *, query):

            query = query.strip()
            
            with open("bully messages.txt","r") as file:
                content = file.read()

            content = content.split("\n")
            botMessage = random.choice(content)

            author = '{0.author.mention}'.format(ctx.message)
            await ctx.send(botMessage.format(author,query))


    @commands.command(name="kill", help="kill @Person - You virtually kill a person")
    async def kill(self, ctx, *, query):
        author = '{0.author.mention}'.format(ctx.message)
        await ctx.send("Killing is bad, {}".format(author))
