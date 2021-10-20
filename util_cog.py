#pip install prsaw
#pip install -U deep_translator

import discord
from discord.ext import commands
import random
import json 
from prsaw import RandomStuff
import asyncio
from deep_translator import GoogleTranslator

with open("apiKey.txt","r") as file:
    key = file.read()

chatbot = RandomStuff(api_key=key)


class util_cog(commands.Cog):

    @commands.command(name="Random", help="Random a b - Provides a random number between a and b")
    async def random(self, ctx, *, query = ""):

        try:
            values = query.strip().split(" ")

            if int(values[0]) > int(values[1]):
                values[0],values[1] = values[1],values[0]

            await ctx.send("A random number between {} and {} is {}".format(values[0],values[1],random.randint(int(values[0]),int(values[1])+1)))
        
        except:
            await ctx.send("How do you expect me to give you a random integer when you don't input 2 digits")



    @commands.command(name="Bully", help="Bully @Person - You virtually bully a person in a unique way")         # TO FIX
    async def bully(self, ctx, *, query = ""):
        
        try:
            if (query != ""):
                query = query.strip()
            
                with open("bully messages.txt","r") as file:
                    content = file.read()

                content = content.split("\n")
                botMessage = random.choice(content)

                author = '{0.author.mention}'.format(ctx.message)
                await ctx.send(botMessage.format(author,query))

            else:
                await ctx.send("Don't bully yourself... {}".format('{0.author.mention}'.format(ctx.message)))

        except:
            await ctx.send("Some error happened, make sure the syntax is correct.")


    @commands.command(name="Kill", help="Kill @Person - You virtually kill a person")
    async def kill(self, ctx, *, query = ""):

        author = '{0.author.mention}'.format(ctx.message)
        await ctx.send("Killing is bad, {}".format(author))


    @commands.command(name="Mock", help="mOcKs ThE tExT")
    async def mock(self, ctx, *, query = ""):

        finalString = ""
        query = query.split(" ")

        if len(query[0]) % 2 == 0:
            step = 0
        else:
            step = 1

        for i in range(len(query)):

            for j in range(len(query[i])):

                if step == 0:
                    finalString = finalString + query[i][j].lower()
                    step += 1

                else:
                    finalString = finalString + query[i][j].upper()
                    step -= 1

            finalString = finalString + " "

        await ctx.send(finalString)


    @commands.command(name="Chatbot", help="Want to talk to Zul Krauss? Now you can!")
    async def chatbot(self, ctx, *, message):
        
        message = str(message)

        await ctx.send(chatbot.get_ai_response(message)[0]["message"])


    @commands.command(name="Pun", help="Want some puns?")
    async def pun(self, ctx):

        joke = chatbot.get_joke("pun")

        try:

            await ctx.send("{}\n{}".format(joke["setup"],joke["delivery"]))
        
        except:

            try:

                await ctx.send("{}".format(joke["joke"]))

            except: 

                await ctx.send("{}    - IF YOU FIND THIS FORMAT, SEND ME A PICTURE OF IT Planta#9305".format(joke))


    @commands.command(name="PJoke", help="Programming jokes!")
    async def pjoke(self, ctx):

        joke = chatbot.get_joke("dev")

        try:

            await ctx.send("{}\n{}".format(joke["setup"],joke["delivery"]))
        
        except:

            try:

                await ctx.send("{}".format(joke["joke"]))

            except: 

                await ctx.send("{}    - IF YOU FIND THIS FORMAT, SEND ME A PICTURE OF IT Planta#9305".format(joke))


    @commands.command(name="Spooky", help="\"Spooky\" stuff")
    async def spooky(self, ctx):

        joke = chatbot.get_joke("spooky")

        try:

            await ctx.send("{}\n{}".format(joke["setup"],joke["delivery"]))
        
        except:

            try:

                await ctx.send("{}".format(joke["joke"]))

            except: 

                await ctx.send("{}    - IF YOU FIND THIS FORMAT, SEND ME A PICTURE OF IT Planta#9305".format(joke))


    @commands.command(name="RemindMe", help="Reminds you in x minutes of something you want to be reminded of")
    async def remindme(self, ctx, minutes, *, message):

        try:
        
            minutes = float(minutes)
            minutes = minutes*60

            if minutes/60 != 1:
                s = "s"
            else:
                s = ""

            await ctx.send("Sure! I'll remind you")

            await asyncio.sleep(minutes)

            await ctx.author.send("{} I've been told to remind you in {} miunte{} of: \"{}\"".format(ctx.author.mention, minutes/60, s, message))

        except:

            await ctx.send("Wrong syntax, please check the help section of this command")


    @commands.command(name="Translate", help="Transates to your desired language.")
    async def translate(self, ctx, language, *, message):
        
        try:

            translatedMessage = GoogleTranslator(source='auto', target=language).translate(message)

            await ctx.send("I've been asked to translate: {}\nHere you go, this is the translation: {}".format(message,translatedMessage))

        except:

            await ctx.send("Either you are translating into some unheard language or there is a syntax error involved.")