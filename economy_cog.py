import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import pickle
import os


# Rob , Give , Yoink , Beg

def dataFileLoader():

    if os.path.isfile("data.pickle"):

        with open("data.pickle", "rb") as file:
            return pickle.load(file)

    else:
        return dict()

def loadUserData(userID):

    data = dataFileLoader()

    if userID not in data:
        return Data(0, 0)

    return data[userID]

def saveUserData(userID, userData):

    data = dataFileLoader()

    data[userID] = userData

    with open("data.pickle", "wb") as file:
        pickle.dump(data, file)



class Data():

    def __init__(self, wallet, bank):
        self.wallet = wallet
        self.bank = bank


class econ_cog(commands.Cog):

    @commands.command(name="work", help="work - Gives you a random amount of currency")
    @commands.cooldown(1,3600,commands.BucketType.user)
    async def work(self, ctx):

        income = random.randint(2,1000)

        userData = loadUserData(ctx.author.id)
        userData.wallet = userData.wallet + income
        saveUserData(ctx.author.id,userData)

        await ctx.send("You earned {} Krauss Coins!".format(income))

        
    @commands.command(name="balance", help="balance - Shows your balance, both in bank and in your wallet")
    async def balance(self, ctx, *, query = ""):
        
        if (query == ""):
            userData = loadUserData(ctx.author.id)

            embed = discord.Embed(title = "{}'s balance".format(ctx.author.display_name))
            embed.add_field(name="Wallet",value = str(userData.wallet))
            embed.add_field(name="Bank",value = str(userData.bank))

            await ctx.send(embed=embed)

        else:
            await ctx.send("In a real life situation you would not be able to just look into someone else's balance, so neither can you here.")

    @commands.command(name="deposit", help="deposit x - Deposits x amount to your bank")
    async def deposit(self, ctx, *, amount):

        amount = amount.strip()

        try:
            amount = int(amount)

            userData = loadUserData(ctx.author.id)

            if amount <= userData.wallet:

                userData.wallet = userData.wallet - amount
                userData.bank = userData.bank + amount
                saveUserData(ctx.author.id,userData)

                await ctx.send("Successfully deposited {} Krauss Coins!".format(amount))

            else:

                await ctx.send("You don't have enough Krauss Coins to perform this action.")

        except:

            await ctx.send("Some error happened, please use only integer amounts")


    @commands.command(name="withdraw", help="withdraw x - Withdraws x amount of money from your bank")
    async def withdraw(self, ctx, *, amount):

        amount = amount.strip()

        try:
            amount = int(amount)

            userData = loadUserData(ctx.author.id)

            if amount <= userData.bank:

                userData.bank = userData.bank - amount
                userData.wallet = userData.wallet + amount
                saveUserData(ctx.author.id,userData)

                await ctx.send("Successfully withdrawn {} Krauss Coins!".format(amount))

            else:

                await ctx.send("You don't have enough Krauss Coins to perform this action.")

        except:

            await ctx.send("Some error happened, please use only integer amounts")


    @commands.command(name="beg", help="beg - Gives you a random amount of currency")
    @commands.cooldown(1,300,commands.BucketType.user)
    async def beg(self, ctx):

        income = random.randint(0,50)

        if income != 1:
            s = "s"
        else:
            s = ""

        userData = loadUserData(ctx.author.id)
        userData.wallet = userData.wallet + income
        saveUserData(ctx.author.id,userData)

        await ctx.send("Begging got you {} Krauss Coin{}!".format(income,s))


    @commands.command(name="give", help="give @person amount - Donates a part of your money to the person in cause")
    async def give(self, ctx, user: discord.User, amount = None):
        
        user = user.id

        if amount == None:
            await ctx.send("Please enter the amount")

        else:
            try:
                amount = int(amount)

                authorBank = loadUserData(ctx.author.id)
                mentionedBank = loadUserData(user)

                if amount > authorBank.wallet:
                    await ctx.send("You can not give more money than you have in your wallet.")

                else:
                    authorBank.wallet = authorBank.wallet - amount 
                    mentionedBank.wallet = mentionedBank.wallet + amount
                    saveUserData(ctx.author.id,authorBank)
                    saveUserData(user,mentionedBank)
        
            except:
                await ctx.send("Did you misstype the amount? Please only use integers")

        
