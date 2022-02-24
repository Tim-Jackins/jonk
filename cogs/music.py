import discord
from discord.ext import tasks, commands
import youtube_dl
import pafy
import asyncio
from queue import Queue
import os


YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl = youtube_dl.YoutubeDL(YTDL_FORMAT_OPTIONS)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Queue dictionary
        self.qdb = {}
        self.qdb_lock = asyncio.Lock()
        self.song_transition_event = asyncio.Event()

    def handle_end_of_song(self, error):
        self.song_transition_event.set()

    async def get_source(self, url, download=False):
        if download:
            filename = await YTDLSource.from_url(url, loop=None)
            info = ytdl.extract_info(url, download=False)
            i_url = info['formats'][0]['url']
            source = discord.FFmpegPCMAudio(executable="ffmpeg", source=filename)
        else:
            video = pafy.new(url)
            best = video.getbestaudio()
            i_url = best.url
            source = await discord.FFmpegOpusAudio.from_probe(i_url, **FFMPEG_OPTIONS)

        return source

    @tasks.loop(seconds=1)
    async def next_song_checker(self):
        await self.song_transition_event.wait()
        for voice_client in self.bot.voice_clients:
            if not voice_client.is_playing():
                async with self.qdb_lock:
                    q = self.qdb.get(str(voice_client.guild.id))
                    if q:
                        next_song_url = q.get()
                        source = await self.get_source(next_song_url)
                        voice_client.play(source, after=self.handle_end_of_song)
        self.song_transition_event.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        self.next_song_checker.start()

    @commands.command(name='play', help='Play a song by url')
    async def play(self, ctx, url):
        voice_client = ctx.message.guild.voice_client

        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        elif not voice_client:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            voice_client = ctx.message.guild.voice_client

        youtube_start = 'https://www.youtube.com/watch?v='
        if url[:len(youtube_start)] == youtube_start:
            async with ctx.typing():
                if voice_client.is_playing() or voice_client.is_paused():
                    # Add to queue
                    print('adding to the queue')
                    await ctx.send('**Queueing:** {}'.format(pafy.new(url).title))

                    queue_key = str(voice_client.guild.id)
                    async with self.qdb_lock:
                        if not self.qdb.get(queue_key):
                            self.qdb.update({queue_key: Queue(maxsize=int(os.getenv('MAX_QUEUE_SIZE')))})
                        self.qdb[queue_key].put(url)
                else:
                    source = await self.get_source(url)
                    voice_client.play(source, after=self.handle_end_of_song)
                    await ctx.send('**Now playing:** {}'.format(pafy.new(url).title))
        else:
            # Do the search
            pass
        # except Exception as e:
        #     print(e)
        #     await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name='pause', help='Pauses the song')
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send('The bot was not paused.')

    @commands.command(name='queue', help='Display the queue of songs')
    async def queue(self, ctx):
        voice_client = ctx.message.guild.voice_client
        async with self.qdb_lock:
            q = self.qdb.get(str(voice_client.guild.id))
            if q and not q.empty():
                songs = '\n'.join([f'{i+1}: {pafy.new(elem).title}' for i, elem in enumerate(list(q.queue))])
                quote_text = f'Your queue:\n>>> {songs}'
                await ctx.send(quote_text)
            else:
                ctx.send("There's nothing in your queue.")

    @commands.command(name='skip', help='Skips the current song')
    async def skip(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            self.handle_end_of_song('none')
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='clear', help='Clears the queue')
    async def clear(self, ctx):
        voice_client = ctx.message.guild.voice_client
        async with self.qdb_lock:
            q = self.qdb.get(str(voice_client.guild.id))
            if q and not q.empty():
                with q.mutex:
                    q.queue.clear()
                await ctx.send('The queue is cleared')
            else:
                await ctx.send("There's nothing to clear")
