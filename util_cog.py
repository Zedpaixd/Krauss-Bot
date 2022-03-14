#pip install prsaw
#pip install -U deep_translator

import discord
from discord.ext import commands
import random
import json 
import os
from pathlib import Path
from prsaw import RandomStuff
import asyncio
from deep_translator import GoogleTranslator
import requests

with open("apiKey.txt","r") as file:
    key = file.readline().strip()
    key2 = file.readline().strip()


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
                
                with open(str(Path().absolute())+r"\Message Templates\bully messages.txt","r") as file:
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

        url = "https://random-stuff-api.p.rapidapi.com/ai"

        querystring = {"msg":message,"bot_name":"Zul Krauss","bot_gender":"rat","bot_master":"Zedpaixd","bot_age":"1","bot_location":"Cyber World","bot_birth_year":"2021","bot_birth_date":"21st August 2021","bot_birth_place":"Cyber World","bot_favorite_color":"Purple","bot_favorite_book":"The Tempest","bot_favorite_band":"iPrevail","bot_favorite_artist":"Kaiyko & HYNN","id":random.randint(0,500000)}

        headers = {
                'authorization': key,
                'x-rapidapi-host': "random-stuff-api.p.rapidapi.com",
                'x-rapidapi-key': key2
                }

        response = requests.request("GET", url, headers=headers, params=querystring)

        kraussReply = json.loads(response.text)

        await ctx.send(kraussReply["AIResponse"])


    @commands.command(name="Joke", help="Want some jokes? What tag do you want? (CaSe sEnSiTiVe) attitude, life, men, women, sport, beauty, sarcastic, marriage, people, car, animal, dirty, love, IT, stupid, motivational, money, intelligence, insults, rude, ugly, time, work, communication, hate, Father's Day, christian, God, family, political, doctor, food, kids, Christmas, flirty, mistake, fighting, age, retirement, success, friendship, happiness, motorcycle, alcohol, school, health, sex, Halloween, puns, birthday, death, blonde, travel, Valentines, racist, black, gay, drug, fat, best man speech, wedding, New Year, Thanksgiving, graduation, autumn, Easter, Mother's Day, April Fools Day, spring, summer, winter, St. Patrick's Day")
    async def pun(self, ctx, *, jType = ""):

        if jType in ['attitude', 'life', 'men', 'women', 'sport', 'beauty', 'sarcastic', 'marriage', 'people', 'car', 'animal', 'dirty', 'love', 'IT', 'stupid', 'motivational', 'money', 'intelligence', 'insults', 'rude', 'ugly', 'time', 'work', 'communication', 'hate', "Father's Day", 'christian', 'God', 'family', 'political', 'doctor', 'food', 'kids', 'Christmas', 'flirty', 'mistake', 'fighting', 'age', 'retirement', 'success', 'friendship', 'happiness', 'motorcycle', 'alcohol', 'school', 'health', 'sex', 'Halloween', 'puns', 'birthday', 'death', 'blonde', 'travel', 'Valentines', 'racist', 'black', 'gay', 'drug', 'fat', 'best man speech', 'wedding', 'New Year', 'Thanksgiving', 'graduation', 'autumn', 'Easter', "Mother's Day", 'April Fools Day', 'spring', 'summer', 'winter', "St. Patrick's Day"]:

            url = "https://random-stuff-api.p.rapidapi.com/joke"

            querystring = {"type":jType}

            headers = {
                'authorization': key,
                'x-rapidapi-host': "random-stuff-api.p.rapidapi.com",
                'x-rapidapi-key': key2
                }

            req = requests.request("GET", url, headers=headers, params=querystring)

            joke = json.loads(req.text)

            try:

                await ctx.send("{}\n{}".format(joke["setup"],joke["delivery"]))
            
            except:

                try:

                    await ctx.send("{}".format(joke["joke"]))

                except: 

                    await ctx.send("{}    - IF YOU FIND THIS FORMAT, SEND ME A PICTURE OF IT Planta#9305".format(joke))

        else:

            await ctx.send ("Invalid type! Do \"<prefix>help joke\" to see all possible types.")


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


    @commands.command("InThisHouseWe", help="We did... what?")            #REQUESTED
    async def InThisHouse(self, ctx, *, message):

        await ctx.send("┏┓\n┃┃╱╲ in\n┃╱╱╲╲ this\n╱╱╭╮╲╲house\n▔▏┗┛▕▔ we\n╱▔▔▔▔▔▔▔▔▔▔╲\n{}\n╱╱┏┳┓╭╮┏┳┓ ╲╲\n▔▏┗┻┛┃┃┗┻┛▕▔".format(" "*(int(10-min((len(message)/8),20))) + message))


    @commands.command("SayD", help="Make Krauss Bot say something and delete your message after")
    async def SayD(self, ctx, *, message):

        await ctx.send(message)
        await ctx.message.delete()


    @commands.command("Say", help="Make Krauss Bot say something")
    async def Say(self, ctx, *, message):

        await ctx.send(message)
