import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import pickle
import os


# Yoink

store = [[{"name":"Bomb"},{"price":500},{"description":"Chance of explosion upon you being robbed, saving your money"}],
         [{"name":"Donation to charity"},{"price":99999},{"description":"What the name says"}],
         [{"name":"Nothing"},{"price":2},{"description":"Genuinely nothing, what are you looking at"}]]


def dataFileLoader():

    if os.path.isfile("data.pickle"):

        with open("data.pickle", "rb") as file:
            return pickle.load(file)

    else:
        return dict()


def loadUserData(userID):

    data = dataFileLoader()

    if userID not in data:
        return Data(0, 0, {})

    return data[userID]


def saveUserData(userID, userData):

    data = dataFileLoader()

    data[userID] = userData

    with open("data.pickle", "wb") as file:
        pickle.dump(data, file)


def canBuy(ctx, itemName):
        
    itemName = itemName.lower()
    _name = ""

    for item in store:

        name = item[0]["name"].lower()

        if name == itemName:

            _name = name
            price = item[1]["price"]
            break

    if _name == "":
            
        return False,0

    authorBank = loadUserData(ctx.author.id)

    if authorBank.wallet < price:
            
        return False,0

    return True,price
        






class Data():

    def __init__(self, wallet, bank, items):
        self.wallet = wallet
        self.bank = bank
        self.items = {}
        






class econ_cog(commands.Cog):

    @commands.command(name="Work", help="Gives you a random amount of currency")
    @commands.cooldown(1,3600,commands.BucketType.user)
    async def work(self, ctx):

        income = random.randint(2,1000)

        userData = loadUserData(ctx.author.id)
        userData.wallet = userData.wallet + income
        saveUserData(ctx.author.id,userData)

        await ctx.send("You earned {} Krauss Coins!".format(income))


        
    @commands.command(name="Balance", aliases=["bank","money","wallet"], help="Shows your balance, both in bank and in your wallet")
    async def balance(self, ctx, *, query = ""):
        
        if (query == ""):
            userData = loadUserData(ctx.author.id)

            embed = discord.Embed(title = "{}'s balance".format(ctx.author.display_name))
            embed.add_field(name="Wallet",value = str(userData.wallet))
            embed.add_field(name="Bank",value = str(userData.bank))

            await ctx.send(embed=embed)

        else:
            await ctx.send("In a real life situation you would not be able to just look into someone else's balance, so neither can you here.")



    @commands.command(name="Inventory", aliases=["bag","stash","backpack"], help="Shows your inventory")
    async def inventory(self, ctx, *, query = ""):

        if (query == ""):
            userData = loadUserData(ctx.author.id)

            embed = discord.Embed(title = "{}'s inventory".format(ctx.author.display_name))
            
            for item in userData.items:

                embed.add_field(name=item, value=str(userData.items[item]))

            await ctx.send(embed=embed)

        else:
            await ctx.send("In a real life situation you would not be able to just look into someone else's balance, so neither can you here.")



    @commands.command(name="Deposit", help="Deposits x amount to your bank")
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



    @commands.command(name="Withdraw", help="Withdraws x amount of money from your bank")
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



    @commands.command(name="Beg", help="Gives you a random amount of currency")
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



    @commands.command(name="Give", help="Donates a part of your money to the person in cause")
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



    @commands.command(name="Rob", help="You attempt robbing a person")
    @commands.cooldown(1,60,commands.BucketType.user)
    async def rob(self, ctx, user: discord.User):

        user = user.id
        authorBank = loadUserData(ctx.author.id)
        mentionedBank = loadUserData(user)

        if (mentionedBank.bomb == 1):

            chance = random.randint(1,100)

            if (chance <= 50):

                await ctx.send("The person who you are trying to rob's bomb has exploded making a loud noise. To not be caught you ran away")
                mentionedBank.bomb = 0

            else:

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



    @commands.command(name="BankRob", help="You try robbing a bank. Big risk but big payoff")
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



    @commands.command(name="Shop", aliases = ["store"], help="Shows you the items we currently have in store")
    async def shop(self,ctx):

        embedMsg = discord.Embed(title = "Shop")

        for item in store:
            name = item[0]["name"]
            price = item[1]["price"]
            description = item[2]["description"]

            embedMsg.add_field(name=name, value="Price: {} Krauss Coins \n Description:  {}".format(price,description))

        await ctx.send(embed = embedMsg)



    @commands.command(name="Buy", aliases = ["purchase"], help="Buys an item from the availables one in the shop")
    async def buy(self, ctx, *, query=""):

        buyable,price = canBuy(ctx, query.strip())

        if buyable == True:

            authorBank = loadUserData(ctx.author.id)

            try:
                authorBank.items[query] = authorBank.items[query] + 1

            except:
                authorBank.items[query] = 1

            authorBank.wallet = authorBank.wallet - price
            saveUserData(ctx.author.id,authorBank)

            await ctx.send("You transaction was successful.")

        else:

            await ctx.send("Either you misspelled the name or you don't have enough money in your wallet.")



# Throw (throws item away) | GiveItem 

    