import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import pickle
import os


# Deposit , Rob , Give

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
    async def work(self, ctx):

        income = random.randint(2,1000)

        userData = loadUserData(ctx.author.id)
        userData.wallet = userData.wallet + income
        saveUserData(ctx.author.id,userData)

        await ctx.send("You earned {} Krauss Coins!".format(income))

        
    @commands.command(name="balance", help="balance - Shows your balance, both in bank and in your wallet")
    async def balance(self, ctx):

        userData = loadUserData(ctx.author.id)

        embed = discord.Embed(title = "{}'s balance".format(ctx.author.display_name))
        embed.add_field(name="Wallet",value = str(userData.wallet))
        embed.add_field(name="Bank",value = str(userData.bank))

        await ctx.send(embed=embed)

    @commands.command(name="deposit", help="deposit x - Deposits x amount to your bank")
    async def deposit(self, ctx, *, amount):

        amount = amount.strip()

        try:
            amount = int(amount)

            userData = loadUserData(ctx.author.id)
            userData.wallet = userData.wallet - amount
            userData.bank = userData.bank + amount
            saveUserData(ctx.author.id,userData)

            await ctx.send("Successfully deposited {} Krauss Coins!".format(amount))

        except:

            await ctx.send("Some error happened, please use only integer amounts")