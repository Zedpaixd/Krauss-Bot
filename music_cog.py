#pip install youtube_dl
#pip install ffmpeg

import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


class music_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
        # bot related variables
        self.is_playing = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.np = ""
        self.vc = ""


     # youtube song search
    def search_yt(self, query):

        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % query, download=False)['entries'][0]

            except: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}


    def play_next(self):

        if len(self.music_queue) > 0:
            self.is_playing = True

            # getting the url of the first song and removing it from the queue
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False


    async def play_music(self, ctx):

        if len(self.music_queue) > 0:

            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            # connect to voice channel if not already in one

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()

            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)

            self.np = self.music_queue[0][0]['title']

            await ctx.send("Now playing: {}".format(self.np))

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected!")


    @commands.command(name="Play", help="play {link/name} - Plays a selected song from youtube")
    async def play(self, ctx, *args):

        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel

        # voice channel check so the bot joins your vc
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")

        else:
            song = self.search_yt(query)

            if type(song) == type(True):
                await ctx.send("Some error occured, please try a different search. This could be due to playlist or a livestream format.")
            
            else:
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)


    @commands.command(name="Queue", help="queue - Displays the current songs in queue")
    async def queue(self, ctx):

        retval = ""

        for i in range(0, len(self.music_queue)):
            retval += str(i+1) + ". " + self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)

        else:
            await ctx.send("No music in queue")


    @commands.command(name="Skip", help="Skip - Skips the current song being played")
    async def skip(self, ctx):

        if self.vc != "" and self.vc:
            self.vc.stop()

            # playing next song, if there is any
            try:
                await self.play_music(ctx)

            except:
                pass


    @commands.command(name="Pause", help="pause - Pauses the current song being played")
    async def pause(self,ctx):

        if self.vc != "" and self.vc:
            self.vc.pause()


    @commands.command(name="Resume", help="resume - Resumes the current song being played")
    async def resume(self,ctx):

        if self.vc != "" and self.vc:
            self.vc.resume()


    @commands.command(name="Disconnect", help="disconnect - Leaves the voice channel")
    async def disconnect(self, ctx):

         await ctx.voice_client.disconnect()
         await ctx.send("Disconnected!")