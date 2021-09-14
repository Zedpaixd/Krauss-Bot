import random
from discord.ext import commands
import discord
from nltk.corpus import words

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

    @commands.command(name="hangman", help="hangman letter/word - Guesses a letter / the word")
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

    @commands.command(name="rps", help="rps rock/paper/scissors - you play a game of RPS against the AI")
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

            if (user < comp and abs(user - comp) == 1) or (user == 2 and comp == 0):  #Yep... don't ask about the latter
                gameResult = "You win!"

            elif user == comp:
                gameResult = "You two tie."

            else:
                gameResult = "You lost."

            await ctx.send("You picked **{}** and the AI picked **{}**. {}".format(choice,AI,gameResult))


