"""Conatains the cog for handling music commands"""
# pylint: disable=no-self-use

import logging
from typing import Dict
import asyncio
from queue import Queue
import os
from discord.ext import tasks, commands
import pafy


from .utils import is_youtube, get_source, get_yt_result_url

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE"))


class MusicHandler(commands.Cog):
    """Cog for handling music commands"""

    def __init__(self, bot):
        self.bot = bot
        test_queue = Queue(maxsize=MAX_QUEUE_SIZE)
        test_queue.put("https://www.youtube.com/watch?v=XRP9k9nlAfE")
        self.qdb: Dict[str, "Queue[str]"] = {"941817356596945017": test_queue}
        self.qdb_lock = asyncio.Lock()
        self.song_transition_event = asyncio.Event()

    def handle_end_of_song(self, error: Exception):
        """Syncronous handler for song transitions"""
        if error:
            logger.error(error)
        self.song_transition_event.set()

    @tasks.loop(seconds=1)
    async def next_song_checker(self):
        """
        Creates and plays a new source based on what's in the queue
        """
        await self.song_transition_event.wait()
        for voice_client in self.bot.voice_clients:
            if not voice_client.is_playing():
                async with self.qdb_lock:
                    _queue = self.qdb.get(str(voice_client.guild.id))
                    if _queue and not _queue.empty():
                        next_song_url = _queue.get()
                        source = await get_source(next_song_url)
                        voice_client.play(source, after=self.handle_end_of_song)
        self.song_transition_event.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Start the song transition handler task when thhe bot starts up.
        """
        self.next_song_checker.start()  # pylint: disable=no-member

    # 1 per user per 2s
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(name="play", help="Play a song by url")
    async def play(self, ctx, *args):
        """Play a song or radio by url / Search and play a song from text"""
        voice_client = ctx.message.guild.voice_client

        if not ctx.message.author.voice:
            await ctx.send(
                f"{ctx.message.author.name} is not connected to a voice channel"
            )
            return

        if not voice_client:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            voice_client = ctx.message.guild.voice_client

        youtube_start = "https://www.youtube.com/watch?v="
        if args[0][: len(youtube_start)] != youtube_start:
            if args[0][:4] == "http":
                # We've received a non-youtube URL
                url = args[0]
            else:
                # Set url to first search result
                query = "+".join(args)
                url = await get_yt_result_url(query)
        else:
            url = args[0]

        if voice_client.is_playing() or voice_client.is_paused():
            # If bot is already playing a song add it to the queue
            print("adding to the queue")
            if is_youtube(url):
                await ctx.send(f"**Queueing:** {pafy.new(url).title}")

            queue_key = str(voice_client.guild.id)
            async with self.qdb_lock:
                if not self.qdb.get(queue_key):
                    self.qdb.update({queue_key: Queue(maxsize=MAX_QUEUE_SIZE)})
                self.qdb[queue_key].put(url)
        else:
            # If nothing is playing just play the song
            source = await get_source(url)
            voice_client.play(source, after=self.handle_end_of_song)
            if is_youtube(url):
                await ctx.send(f"**Now playing:** {pafy.new(url).title}")

    # 1 per user per 2s
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(name="pause", help="Pauses the song")
    async def pause(self, ctx):
        """Pauses the song"""
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    # 1 per user per 2s
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(name="resume", help="Resumes the song")
    async def resume(self, ctx):
        """Resumes the song"""
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            if not voice_client.is_playing():
                async with self.qdb_lock:
                    _queue = self.qdb.get(str(voice_client.guild.id))
                    if _queue and not _queue.empty():
                        next_song_url = _queue.get()
                        source = await get_source(next_song_url)
                        voice_client.play(source, after=self.handle_end_of_song)
                    else:
                        await ctx.send("The bot was not paused.")
            else:
                await ctx.send("The bot was not paused.")

    @commands.command(name="queue", help="Display the queue of songs")
    async def queue(self, ctx):
        """Display the queue of songs for that guild's bot"""
        guild = ctx.message.guild
        async with self.qdb_lock:
            _queue = self.qdb.get(str(guild.id))
            if _queue and not _queue.empty():
                songs = "\n".join(
                    [
                        f"{i+1}: {pafy.new(elem).title}"
                        for i, elem in enumerate(list(_queue.queue))
                    ]
                )
                quote_text = f"Your queue:\n>>> {songs}"
                await ctx.send(quote_text)
            else:
                await ctx.send("There's nothing in your queue.")

    # 1 per user per 2s
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(name="skip", help="Skips the current song")
    async def skip(self, ctx):
        """Skips the current song"""
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            self.handle_end_of_song(None)
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    # 1 per user per 10s
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="clear", help="Clears the queue")
    async def clear(self, ctx):
        """Clears the queue for that guild's bot"""
        voice_client = ctx.message.guild.voice_client
        async with self.qdb_lock:
            _queue = self.qdb.get(str(voice_client.guild.id))
            if _queue and not _queue.empty():
                with _queue.mutex:
                    _queue.queue.clear()
                await ctx.send("The queue is cleared")
            else:
                await ctx.send("There's nothing to clear")
