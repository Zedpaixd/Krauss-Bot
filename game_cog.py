import random
from discord.ext import commands
import discord
from nltk.corpus import words
import asyncio
import time



def card_deck():

    card_values = ['2','3','4','5','6','7','8','9','10','J','Q','K']
    card_types = ['Hearts','Spades','Clubs','Diamonds']
    deck = []

    for i in card_types:

        for j in card_values:

            deck.append(j + ' of ' + i)

    return deck


class Blackjack:

    def __init__(self):
        
        self.playerTotal = 0
        self.dealerTotal = 0
        self.dealerShownTotal = 0
        self.initalizeGame = False
        self.card_deck = card_deck()
        self.playerHand = ""
        self.dealerHand = ""
        self.dealerShownHand = ""


    def card_value(self,card):

        if card[:1] in ('2','3','4','5','6','7','8','9'):
            return int(card[:1])

        elif card[:1] in ('J','Q','K','1'):
                    return int(10)


    def newCard(self,deck):

        return deck[random.randint(0,len(deck)-1)]


    def removeCard(self,deck,card):

        return deck.remove(card)


    def getTotals(self):
        
        return self.playerTotal,self.dealerTotal



bjGames = {}

class BlackjackGame:

    currentGame = None

    def run(self, playerID, command):

        self.getGameID(playerID)

        if (command.lower() == "start") and self.currentGame.initalizeGame == False:

            card1 = self.currentGame.newCard(self.currentGame.card_deck)
            self.currentGame.removeCard(self.currentGame.card_deck,card1)
            card2 = self.currentGame.newCard(self.currentGame.card_deck)
            self.currentGame.removeCard(self.currentGame.card_deck,card2)
            self.currentGame.playerTotal = self.currentGame.card_value(card1) + self.currentGame.card_value(card2)
            self.currentGame.playerHand = self.currentGame.playerHand + "{} , {}".format(card1,card2)

            dealercard1 = self.currentGame.newCard(self.currentGame.card_deck)
            self.currentGame.removeCard(self.currentGame.card_deck,dealercard1)
            self.currentGame.dealerShownTotal = self.currentGame.card_value(dealercard1)
            dealercard2 = self.currentGame.newCard(self.currentGame.card_deck)
            self.currentGame.removeCard(self.currentGame.card_deck,dealercard2)
            self.currentGame.dealerTotal = self.currentGame.card_value(dealercard1) + self.currentGame.card_value(dealercard2)
            self.currentGame.dealerHand = self.currentGame.dealerHand + "{} , {}".format(dealercard1,dealercard2)
            self.currentGame.dealerShownHand = self.currentGame.dealerShownHand + "{} and one other card facing downwards".format(dealercard1)

            self.currentGame.initalizeGame = True

            return self.currentGame.initalizeGame,self.currentGame.playerTotal,self.currentGame.dealerShownTotal,self.currentGame.playerHand,self.currentGame.dealerShownHand

        elif (command.lower() == "hit"):

            drawnCard = self.currentGame.newCard(self.currentGame.card_deck)
            self.currentGame.removeCard(self.currentGame.card_deck,drawnCard)
            drawnValue = self.currentGame.card_value(drawnCard)
            self.currentGame.playerTotal = self.currentGame.playerTotal + int(drawnValue)

            return self.currentGame.initalizeGame,self.currentGame.playerTotal,self.currentGame.dealerShownTotal,self.currentGame.playerHand,self.currentGame.dealerShownHand

        elif (command.lower() == "hold"):

            while self.currentGame.dealerTotal < 17:

                newDraw = self.currentGame.newCard(self.currentGame.card_deck)
                self.currentGame.removeCard(self.currentGame.card_deck,newDraw)
                newDrawValue = self.currentGame.card_value(newDraw)
                self.currentGame.dealerTotal = self.currentGame.dealerTotal + newDrawValue
            
                
            return self.currentGame.initalizeGame,self.currentGame.playerTotal,self.currentGame.dealerTotal,self.currentGame.playerHand,self.currentGame.dealerHand


        self.save(playerID)



    def getGameID(self, playerID):

        if playerID in bjGames.keys():
            self.currentGame = bjGames[playerID]

            if self.currentGame is None:
                self.initializeGame(playerID)

        else:
            self.initializeGame(playerID)



    def initializeGame(self, playerID):

        self.currentGame = Blackjack()
        self.save(playerID)



    def save(self, playerID):

        bjGames[playerID] = self.currentGame


    async def reset(self, playerID):

        bjGames.pop(playerID)
















class Hangman:

    word = ""
    wordProgress = "_You don't know anything about the word and you want to guess already? Don't get ahead of yourself_"
    guesses = list()



    def __init__(self, word):

        self.word = word
        self.lives = 8
        self.guesses = list()



    def isWordGuessed(self,word):

        if self.word == word:
            return True

        else:
            return False



    def gameStateCheck(self, guessedWord):

        gameOver = False
        gameWon = False

        if self.lives <= 0:
            gameOver = True

        won = self.isWordGuessed(guessedWord)

        if won == True:
            gameOver = True

        return gameOver, won



    def guess(self, letter):
        
        letter = letter.lower()
        self.wordProgress = ""

        if letter not in self.word.lower() and letter not in self.guesses:
            self.lives = self.lives - 1

        for character in self.word.lower():

            if letter == character or character in self.guesses:
                self.wordProgress = self.wordProgress + character

            else:
                self.wordProgress = self.wordProgress + "\_ "
        
        if letter not in self.guesses:
            self.guesses.append(letter)

            

games = {}

class HangmanGame:

    currentGame = None

    def returnWord(self):

        return self.currentGame.word



    def returnGuesses(self):

        return ",".join(self.currentGame.guesses)



    def returnProgress(self):

        return self.currentGame.wordProgress



    def returnLives(self):

        return self.currentGame.lives



    def run(self, playerID, guess):

        self.getGameID(playerID)
        gameState, won = self.playRound(guess)
        self.save(playerID)

        return gameState, won



    def playRound(self, guess):

        isWord = False

        if len(guess) == 1:
            pass

        elif len(guess) >= 1:
            isWord = True

        else:
            return None, None

        if isWord == False:
            self.currentGame.guess(guess)

        if "_" not in self.currentGame.wordProgress:
            gameState, won = True, True

        else:
            gameState, won = self.currentGame.gameStateCheck(guess)

            if ((gameState, won) != (True, True)) and isWord == True:
                self.currentGame.lives = self.currentGame.lives - 1
                gameState, won = self.currentGame.gameStateCheck(guess)

               

        return gameState, won



    def getGameID(self, playerID):

        if playerID in games.keys():
            self.currentGame = games[playerID]

            if self.currentGame is None:
                self.initializeGame(playerID)

        else:
            self.initializeGame(playerID)



    def getWord(self):

        wordlist = words.words()

        return random.choice(wordlist).lower()



    def initializeGame(self, playerID):

        gameWord = self.getWord()
        self.currentGame = Hangman(gameWord)
        self.save(playerID)



    def save(self, playerID):

        games[playerID] = self.currentGame



    async def reset(self, playerID):

        games.pop(playerID)




class game_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Hangman", help="hangman letter/word - Guesses a letter / the word")
    async def hangman(self, ctx, guess: str):

        playerID = ctx.author.id
        hangmanUniqueInstance = HangmanGame()
        gameState, won = hangmanUniqueInstance.run(playerID, guess)

        if gameState:
            endMessage = "You lost."

            if won:
                endMessage = "You won!"

            endMessage = endMessage + " The word was {}".format(hangmanUniqueInstance.returnWord())

            await ctx.send(endMessage)
            await hangmanUniqueInstance.reset(playerID)

        else:
            await ctx.send("Progress: {}\nGuesses: {}\nLives: {}".format(hangmanUniqueInstance.returnProgress(),hangmanUniqueInstance.returnGuesses(),hangmanUniqueInstance.returnLives()))

    @commands.command(name="Rps", help="rps rock/paper/scissors - you play a game of RPS against the AI")
    async def rps(self, ctx, *, choice = ""):

        choice = choice.strip().lower()
        values = {"scissors": 1,
                  "paper": 2,
                  "rock": 0}

        if choice not in ["rock", "paper", "scissors"]:
            await ctx.send("Did you misstype? Please write only rock, paper or scissors.")
        
        else:
            AI = random.choice(["rock", "paper", "scissors"])

            user = values[choice]
            comp = values[AI]

            gameResult = ""

            #if (user < comp and abs(user - comp) == 1) or (user == 2 and comp == 0):  #Yep... don't ask about the latter
            if user == (comp-1)%3:
                gameResult = "You win!"

            elif user == comp:
                gameResult = "You two tie."

            else:
                gameResult = "You lost."

            await ctx.send("You picked **{}** and the AI picked **{}**. {}".format(choice,AI,gameResult))


    @commands.command(name="Bj", aliases=["blackjack"], help="Blackjack game. Use !Bj {start,hit,hold}")
    async def bj(self, ctx, *, command):

            
        try:

            uniqueInstance = BlackjackGame()
            gameState,playerHand,dealerHand,playerCards,dealerCards = uniqueInstance.run(ctx.author.id, command)
            

            if gameState == True:

                if playerHand == 21:

                    await ctx.send("Blackjack!! You won!")
                    await uniqueInstance.reset(ctx.author.id)

                elif playerHand > 21:

                    await ctx.send("You busted. Dealer wins!")
                    await uniqueInstance.reset(ctx.author.id)

                elif dealerHand > 21:

                    await ctx.send("Dealer busted. You win!")
                    await uniqueInstance.reset(ctx.author.id)

                elif dealerHand == 21:

                    await ctx.send("Dealer gets a blackjack!! You lost.")
                    await uniqueInstance.reset(ctx.author.id)

                elif command.lower() == "hold":
                    
                    if dealerHand > playerHand:

                        await ctx.send("With a total of {} to {}, the dealer wins!".format(dealerHand,playerHand))

                    elif playerHand > dealerHand:

                        await ctx.send("You won with a total of {} to {}!".format(playerHand,dealerHand))

                    else:

                        await ctx.send("Tie!")

                    await uniqueInstance.reset(ctx.author.id)

                elif (command.lower() == "hit") and playerHand < 21 and dealerHand < 21:

                    await ctx.send("Your new total is: {} ({})\n The dealer's current total is: {} ({})\n What is your next move? (Hit/Hold)".format(playerHand,playerCards,dealerHand,dealerCards))

                elif (command.lower() == "start"):

                    await ctx.send("Your total is: {} ({})\n The dealer's total is: {} ({})\n What is your next move? (Hit/Hold)".format(playerHand,playerCards,dealerHand,dealerCards))

            else:

                await ctx.send("You may wanna start the game first.")

                


        except:
                
            await ctx.send("Syntax Error. Check if you have a game running already or if you misstyped the command.")
            




