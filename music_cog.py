import discord
from discord.ext import commands

from youtube_dl import YoutubeDL
import random


class music_cog(commands.Cog):
    

    def __init__(self, bot):
        self.bot = bot
        self.test = ['https://www.youtube.com/watch?v=BD2ypP3Xwq8&list=PL3zKUp2BPbX41b92Evdp0Ju-p2sAHsbsE&index=21', 'https://www.youtube.com/watch?v=7UGEL_CiRQQ&list=PL3zKUp2BPbX41b92Evdp0Ju-p2sAHsbsE&index=23']
        #all the music related stuff
        self.is_playing = False
        self.is_idling = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""


    # returns a song title random chosen from idle_songs.txt
    def get_next_idle_song(self):
        return random.choice(list(open('peep_songs/idle_songs.txt', encoding="utf-8")))


    def get_voice_channel(self, ctx):
        try:
            voice_channel = ctx.author.voice.channel
            #self.vc = voice_channel
        except Exception:
            voice_channel = None

     #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']
        

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
        
    # infinite loop checking 
    async def play_music(self, ctx):
        print("In play_musci)")
        if len(self.music_queue) > 0:
            self.is_playing = True
            print("CTX:", ctx)
            print("SELF.VC: ", self.vc)
            print("SELF.VC (list): ", self.music_queue[0][1])

            m_url = self.music_queue[0][0]['source']
  
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #changes activity to song title
            
            song_title = self.music_queue[0][0]['title']
            await self.bot.change_presence(activity=discord.Game(name=song_title))
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)
           
            
            
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

            voice_channel = self.get_voice_channel(ctx)
                
            
            if voice_channel is None:
                #you need to be connected so that the bot knows where to go
                await ctx.send("Connect to a voice channel!")

            song = self.search_yt(self.get_next_idle_song()+ " Peep")
            self.music_queue.append([song, voice_channel])
            if self.is_playing == False:
                await self.play_music(ctx)

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, *args):

        if len(args) > 0:
            self.is_idling = False
            query = " ".join(args) + " Lil Peep"
        
            try:
                voice_channel = ctx.author.voice.channel
            except Exception:
                voice_channel = None
            
            if voice_channel is None:
                #you need to be connected so that the bot knows where to go
                await ctx.send("Connect to a voice channel!")
            else:
                song = self.search_yt(query)
                for arg in args:
                    title = song['title'].replace(" ", "")
                    if arg in title:
                        if type(song) == type(True):
                            msg = "Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format."
                        else:
                            msg = "Song added to the queue"
                            self.music_queue.append([song, voice_channel])
                            
                            if self.is_playing == False:
                                await self.play_music()
                    else:
                        msg = "Couldn't find requested song:  " + query
                await ctx.send(msg)
        else:
            self.is_playing = False

            try:
                voice_channel = ctx.author.voice.channel
                #self.vc = voice_channel
            except Exception:
                voice_channel = None
                
            
            if voice_channel is None:
                #you need to be connected so that the bot knows where to go
                await ctx.send("Connect to a voice channel!")

            song = self.search_yt("lil peep star shopping")
            self.music_queue.append([song, voice_channel])
           # self.vc = ctx.author.voice.channel
            await self.play_music(ctx)
            
    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
            
        else:
            await ctx.send("No music in queue")

    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)

 