import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from async_timeout import timeout
import asyncio
from functools import partial
import itertools
import traceback
import sys


YoutubeDLOptions = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'}

FFmpegOptions = {
    'before_options': '-nostdin',
    'options': '-vn'}

YoutubeDL = YoutubeDL(YoutubeDLOptions)


class VoiceConnectionError(commands.CommandError):  # Exception class for connection errors.
    pass


class InvalidVoiceChannel(VoiceConnectionError):    # Exception class for invalid Voice Channels.
    pass


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, author):

        super().__init__(source)

        self.author = author
        self.title = data.get('title')
        


    def __getitem__(self, item: str):   # Access attributes similar to a dict.

        return self.__getattribute__(item)


    @classmethod
    async def createSource(cls, ctx, query: str, *, loop, download=False):
        
        loop = loop or asyncio.get_event_loop()

        try:

            to_run = partial(YoutubeDL.extract_info, url=query, download=download)
            data = await loop.run_in_executor(None, to_run)

            if 'entries' in data: # Take first item from a playlist
                
                data = data['entries'][0]

            await ctx.send("Added {} to the queue!".format(data["title"]))

            if download:
                source = YoutubeDL.prepare_filename(data)

            else:
                return {'webpage_url': data['webpage_url'], 'author': ctx.author, 'title': data['title']}

            return cls(discord.FFmpegPCMAudio(source), data=data, author=ctx.author)

        except:

            await ctx.send("I do not have a dedicated server for myself. When using my music commands please wait for me to finish my previous given command to avoid problems.   \
            \nI have added a 0 second video to replace the faulty song I tried downloading. Please be patient and more specific next time.")

            to_run = partial(YoutubeDL.extract_info, url="https://www.youtube.com/watch?v=BTa2P8Z-O0w", download=download)
            data = await loop.run_in_executor(None, to_run)

            if 'entries' in data: # Take first item from a playlist
                
                data = data['entries'][0]

            if download:
                source = YoutubeDL.prepare_filename(data)

            else:
                return {'webpage_url': data['webpage_url'], 'author': ctx.author, 'title': data['title']}

            return cls(discord.FFmpegPCMAudio(source), data=data, author=ctx.author)


    @classmethod
    async def streamRegathering(cls, data, *, loop):  # Fix for youtube streaming links expiring.

        loop = loop or asyncio.get_event_loop()
        author = data['author']

        to_run = partial(YoutubeDL.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, author=author)


class MusicPlayer(commands.Cog): # Unique instancing for servers. Destroys instance upon no activity in particular server


    __slots__ = ('bot', 'uniqueServer', 'channel', 'cog', 'queue', 'next', 'current', 'np', 'volume')


    def __init__(self, ctx):
        self.bot = ctx.bot
        self.uniqueServer = ctx.guild
        self.channel = ctx.channel
        self.cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = 1
        self.current = None

        ctx.bot.loop.create_task(self.playerLoop())


    async def playerLoop(self): # Music player continuity
        
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try: # Wait for next song in queue. Disconnect after 1 minute if none.
                
                async with timeout(60):  # 60 seconds
                    source = await self.queue.get()

            except asyncio.TimeoutError:
                self.destroy(self.uniqueServer)
                return 

            if not isinstance(source, YTDLSource): # If source was a stream that wasn't downloaded. Regather to prevent the expiration of the stream
               
                try:
                    source = await YTDLSource.streamRegathering(source, loop=self.bot.loop)

                except Exception as e:
                    await self.channel.send('There was an error processing your song.\n')
                    print(e)

                    continue

            source.volume = self.volume
            self.current = source

            try:

                self.uniqueServer.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
                self.np = await self.channel.send('**Now Playing:** {} requested by {}'.format(source.title,source.author))
                await self.next.wait()

            except:

                pass

            
            source.cleanup() # Cleaning FFmpeg up
            self.current = None

            try: # No longer playing the song
                await self.np.delete()

            except discord.HTTPException:
                pass


    def destroy(self, guild): # Fully destroy the player
       
        self.bot.loop.create_task(self.cog.cleanup(guild))
        return 

    


class music_cog(commands.Cog):

    __slots__ = ('bot', 'players')


    def __init__(self, bot):

        self.bot = bot
        self.players = {}


    async def cleanup(self, guild):   # Disconnect from one server

        try:
            await guild.voice_client.disconnect()

        except AttributeError:
            pass

        try:
            del self.players[guild.id]

        except KeyError:
            pass


    async def localChecker(self, ctx): # Instanced check that applies to all music commands

        if not ctx.guild:

            raise commands.NoPrivateMessage
        
        return True


    async def errorHandler(self, ctx, error):   # Error handler

        if isinstance(error, commands.NoPrivateMessage):
            
            try:
                await ctx.send('This command can not be used in Private Messages.')
                return 

            except discord.HTTPException:
                pass

        elif isinstance(error, InvalidVoiceChannel):

            await ctx.send('Error connecting to the voice channel. Make sure you are in a voice channel that I can join.')


    def get_player(self, ctx):  # Get a music player for each server

        try:
            player = self.players[ctx.guild.id]

        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player


    @commands.command(name='Connect', aliases=['join'], help="Joins your voice chat")
    async def connect(self, ctx):

        try:
            channel = ctx.author.voice.channel

        except AttributeError:
            raise InvalidVoiceChannel('No voice channel that I can join.')

        vc = ctx.voice_client

        if vc:

            if vc.channel.id == channel.id:
                return

            try:
                await vc.move_to(channel)

            except asyncio.TimeoutError:
                raise VoiceConnectionError("Moving to channel {} failed. Try again(?)".format(channel))

        else:

            try:
                await channel.connect()

            except asyncio.TimeoutError:
                raise VoiceConnectionError("Connecting to channel {} failed. Try again(?)".format(channel))


    @commands.command(name='Play', help="Plays a selected song from youtube")
    async def play(self, ctx, *, query: str):

        await ctx.trigger_typing()

        vc = ctx.voice_client

        if ctx.author.voice is None:
            await ctx.send("Join a voice chat first.")

        else:
            await ctx.invoke(self.connect)

            player = self.get_player(ctx)

            # If download is False, source will be a dict which will be used later to regather the stream.
            # If download is True, source will be a discord.FFmpegPCMAudio with a volume transformer.
            source = await YTDLSource.createSource(ctx, query, loop=self.bot.loop, download=False)

            await player.queue.put(source)


    @commands.command(name="Pause", help="Pauses the current song being played")
    async def pause(self, ctx):
        
        try:

            channel = ctx.author.voice.channel
            vc = ctx.voice_client

            if(vc.channel.id == channel.id):

                if not vc or not vc.is_playing():

                    await ctx.send('I am not currently playing anything!')
                    return 
        

                elif vc.is_paused():
                    return

                vc.pause()
                await ctx.send('Paused!')

            else:

                await ctx.send("You are not in the same voice channel as me.")

        except:
            await ctx.send('Either the bot is not in a voice chat or you are not in the same voice chat as the bot.')


    @commands.command(name="Resume", help="Resumes the current song being played")
    async def resume(self, ctx):

        try:

            channel = ctx.author.voice.channel
            vc = ctx.voice_client

            if(vc.channel.id == channel.id):

                if not vc or not vc.is_connected():
                    await ctx.send('I am not currently playing anything!')
                    return 

                elif not vc.is_paused():
                    return

                vc.resume()
                await ctx.send('Resumed!')

            else:

                await ctx.send("You are not in the same voice channel as me.")

        except:

            await ctx.send('Either the bot is not in a voice chat or you are not in the same voice chat as the bot.')


    @commands.command(name="Skip", help="Skips the current song being played")
    async def skip(self, ctx):

        try:

            channel = ctx.author.voice.channel
            vc = ctx.voice_client

            if(vc.channel.id == channel.id):

                if not vc or not vc.is_connected():
                    await ctx.send('I am not currently playing anything!')
                    return

                if vc.is_paused():
                    pass

                elif not vc.is_playing():
                    return

                vc.stop()
                await ctx.send('Skipped!')

            else:

                await ctx.send("You are not in the same voice channel as me.")

        except:
            await ctx.send('Either the bot is not in a voice chat or you are not in the same voice chat as the bot.')


    @commands.command(name="Queue", aliases=['q'], help="Displays the current songs in queue")
    async def queue(self, ctx):

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.send('I am not currently connected to voice!')
            return 

        player = self.get_player(ctx)
        if player.queue.empty():
            await ctx.send('There are currently no more queued songs.')
            return 

        upcoming = list(itertools.islice(player.queue._queue, 0, 100)) # Get 5 elements from the queue

        fmt = ""

        for item in upcoming:

            try:
                fmt = fmt + '\n**{}**'.format(item["title"])

            except:
                pass

        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)

        await ctx.send(embed=embed)


    @commands.command(name='nowPlaying', aliases=['np', 'current', 'currentsong', 'playing'], help="Get information about the currently playing song")
    async def nowPlaying(self, ctx):
        
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.send('I am not currently connected to voice!', )
            return 

        player = self.get_player(ctx)
        if not player.current:
            await ctx.send('I am not currently playing anything!')
            return

        try:
            # Remove the previous nowPlaying message.
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.send('Now playing {} | Requested by {}'.format(vc.source.title,vc.source.author))


    @commands.command(name='Volume', aliases=['vol'], help="Changes the volume of the music player")
    async def volume(self, ctx, *, vol: float):

        try:

            channel = ctx.author.voice.channel
            vc = ctx.voice_client

            if(vc.channel.id == channel.id):

                if not vc or not vc.is_connected():
                    await ctx.send('I am not currently connected to voice!', )
                    return

                if vol > 100 or vol < 1:
                    await ctx.send('Please enter a value between 1 and 100.')
                    return

                player = self.get_player(ctx)

                if vc.source:
                    vc.source.volume = vol / 100

                player.volume = vol / 100
                await ctx.send('Volume set to {}%'.format(vol))

            else:

                await ctx.send("You are not in the same voice channel as me.")

        except:
            await ctx.send('Either the bot is not in a voice chat or you are not in the same voice chat as the bot.')





        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """


    @commands.command(name="Disconnect", aliases=['leave'], help="Leaves the voice channel")
    async def stop(self, ctx):

        try:

            channel = ctx.author.voice.channel
            vc = ctx.voice_client

            if(vc.channel.id == channel.id):

                if not vc or not vc.is_connected():
                    await ctx.send('I am not currently playing anything!')
                    return 

                await self.cleanup(ctx.guild)

            else:

                await ctx.send("You are not in the same voice channel as me.")

        except:

            await ctx.send('Either the bot is not in a voice chat or you are not in the same voice chat as the bot.')