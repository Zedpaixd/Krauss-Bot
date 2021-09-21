import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import pickle
import os


# Yoink

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

    @commands.command(name="work", help="Gives you a random amount of currency")
    @commands.cooldown(1,3600,commands.BucketType.user)
    async def work(self, ctx):

        income = random.randint(2,1000)

        userData = loadUserData(ctx.author.id)
        userData.wallet = userData.wallet + income
        saveUserData(ctx.author.id,userData)

        await ctx.send("You earned {} Krauss Coins!".format(income))

        
    @commands.command(name="balance", aliases=["bank","money","wallet"], help="Shows your balance, both in bank and in your wallet")
    async def balance(self, ctx, *, query = ""):
        
        if (query == ""):
            userData = loadUserData(ctx.author.id)

            embed = discord.Embed(title = "{}'s balance".format(ctx.author.display_name))
            embed.add_field(name="Wallet",value = str(userData.wallet))
            embed.add_field(name="Bank",value = str(userData.bank))

            await ctx.send(embed=embed)

        else:
            await ctx.send("In a real life situation you would not be able to just look into someone else's balance, so neither can you here.")


    @commands.command(name="deposit", help="Deposits x amount to your bank")
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


    @commands.command(name="withdraw", help="Withdraws x amount of money from your bank")
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


    @commands.command(name="beg", help="Gives you a random amount of currency")
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


    @commands.command(name="give", help="Donates a part of your money to the person in cause")
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


    @commands.command(name="rob", help="You attempt robbing a person")
    @commands.cooldown(1,60,commands.BucketType.user)
    async def rob(self, ctx, user: discord.User):

        user = user.id
        authorBank = loadUserData(ctx.author.id)
        mentionedBank = loadUserData(user)

        if mentionedBank.wallet < 1:

            await ctx.send("The person doesn't have any money, what are you trying to rob?")

        else:

            outcome = random.randint(1,100)

            if (outcome<15):
            
                robbedAmount = random.randint(mentionedBank.wallet//2,mentionedBank.wallet)

                if robbedAmount != 1:
                    s = "s"

                else:
                    s = ""

                authorBank.wallet = authorBank.wallet + robbedAmount 
                mentionedBank.wallet = mentionedBank.wallet - robbedAmount
                saveUserData(ctx.author.id,authorBank)
                saveUserData(user,mentionedBank)

                await ctx.send("You've stolen a LOT of their belongings. Now if it categorizes as a lot, that is up to you. You've received {} Krauss Coin{}.".format(robbedAmount,s))
        
            elif (outcome < 50):

                robbedAmount = random.randint(0,mentionedBank.wallet//5)

                if robbedAmount != 1:
                    s = "s"

                else:
                    s = ""

                authorBank.wallet = authorBank.wallet + robbedAmount 
                mentionedBank.wallet = mentionedBank.wallet - robbedAmount
                saveUserData(ctx.author.id,authorBank)
                saveUserData(user,mentionedBank)

                await ctx.send("The rob was successful. You've stolen {} Krauss Coin{}.".format(robbedAmount,s))

            elif (outcome < 75):

                await ctx.send("You did not get the chance to steal Krauss Coins from your target, they were on guard.")

            else:

                paidAmount = random.randint(0,authorBank.wallet)

                if paidAmount != 1:
                    s = "s"

                else:
                    s = ""

                authorBank.wallet = authorBank.wallet - paidAmount 
                mentionedBank.wallet = mentionedBank.wallet + paidAmount
                saveUserData(ctx.author.id,authorBank)
                saveUserData(user,mentionedBank)

                await ctx.send("Your rob was unsuccessful. In fact, it went so badly that you were taken to court! You've lost {} Krauss Coin{}.".format(paidAmount,s))


    @commands.command(name="bankRob", help="You try robbing a bank. Big risk but big payoff")
    @commands.cooldown(1,36000,commands.BucketType.user)
    async def bankRob(self, ctx):

        outcome = random.randint(1,100)
        authorBank = loadUserData(ctx.author.id)

        if outcome < 85:

            authorBank.wallet = authorBank.wallet // 4
            authorBank.bank = authorBank.bank // 4
            saveUserData(ctx.author.id,authorBank)

            await ctx.send("Your attempt failed and you've lost most of your money to avoid prison")

        else:

            pay = random.randint(10000,40000)

            authorBank.wallet = authorBank.wallet + pay
            saveUserData(ctx.author.id,authorBank)

            await ctx.send("Your attempt to rob the bank was successful and you've managed to take {} Krauss Coins".format(pay))
