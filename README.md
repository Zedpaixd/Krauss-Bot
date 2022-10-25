# Krauss-Bot
A fully functional but still in development Discord bot with a handful of features and more to be added!
Currently the release is private and may likely remain like that until I find a way to keep it constantly running for cheap.

Given how the bot is open source, you're more than welcome to download the files and run it yourself, as long as I receive any form of credit.


# To Install
First things first, you will need python to be installed and then install the following libraries via the following commands:
- py get-pip.py (Windows) | $ python get-pip.py (Linux / MacOS)   - Installing pip in order to download custom made libraries
- pip install discord.py      - Discord's api
- pip install PyNaCl       - To improve usability, security and speed.
- pip install youtube_dl   - To download songs from YouTube in order to be played via the music bot features of the bot
- pip install ffmpeg       - To allow the bot to actually play the songs in a voice chat
- pip install nltk         - Used to provide a list of words for the hangman game
- pip install prsaw        - Api used to provide human-like bot replies to everyday chat (!!chatbot)
- pip install -U deep_translator - Machine learning translator. Used for the !!translate command

Once you are done with installing the libraries, you will need to create 2 files:
- "botToken.txt" - a simple bot token file. Create it, paste the token in there and save
- "prefixes.json" - a json file where prefixes of servers will be added. If any issues arise with the file, instead of leaving it empty add " {} " inside it, without the quotation marks nor spaces.
- "apiKey.txt" - a txt file containing 2 tokens: #1 is the api key from [their register page](api.pgamerx.com/register) and #2 is the [X-Rapid-API-key from here](https://rapidapi.com/pgamerxdev/api/random-stuff-api); separate them by a new line.

# Bot Features
Will start writing here once more features have been added
