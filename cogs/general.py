"""Contains general cogs for basic tasks, logging, and errors"""
# pylint: disable=no-self-use

import logging
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CommandHandler(commands.Cog):
    """Contains misc bot commands"""

    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Run when the bot is ready"""

        logger.info("===== JONK BEGIN =====")
        logger.info("JONK IS READY")
        logger.info("JONK USER ID: %s", self.bot.user.id)

    @commands.command(name="join", help="Have the bot join your voice channel")
    async def join(self, ctx):
        """Have the bot join your voice channel"""
        if not ctx.message.author.voice:
            await ctx.send(
                f"{ctx.message.author.name} is not connected to a voice channel"
            )
        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()

    @commands.command(name="leave", help="Have the bot leave your voice channel")
    async def leave(self, ctx):
        """Have the bot leave your voice channel"""
        voice_client = ctx.message.guild.voice_client
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name="tell_me_about_yourself", help="A friendly blurb!")
    async def tell_me_about_yourself(self, ctx):
        """Returns a friendly blurb!"""
        await ctx.send("JONK JONK")

    @commands.command(name="status", help="Get bot / server status")
    async def status(self, ctx: commands.Context):
        """Say some stats about the machine we're running on"""
        ret_msg = f"{ctx.author.mention}\n" \
            f"> This guild name: {ctx.guild.name}\n" \
            f"> This guild id: {ctx.guild.id}\n" \
            f"> This channel name: {ctx.channel.name}\n" \
            f"> This channel id: {ctx.channel.id}\n"
        await ctx.send(ret_msg)


class ErrorHandler(commands.Cog):
    """Simple cog for error handling"""

    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """Handler for all command errors"""
        logger.error(error)

        if hasattr(ctx.command, "on_error"):
            return

        age_protected_error = "\x1b[0;31mERROR:\x1b[0m Sign in to confirm your" \
            " age\nThis video may be inappropriate for some users."
        ignored = commands.UserInputError
        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            await ctx.send(error)
        elif isinstance(error, OSError) and str(error) == age_protected_error:
            # Check for age protected video error
            await ctx.send(
                "This video / song is age protected (try searching for a lyric only version)."
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"This command is on a cooldown. Try again in {int(error.retry_after)} second(s)."
            )
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Hello, {ctx.author.mention}. I didn't understand that.")
        else:
            await ctx.send("I encountered a strange error *sad beep boop...*")


class LoggingHandler(commands.Cog):
    """Simple cog for log handling"""

    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Log every message sent to the bot"""
        logger.info(
            "%s, #%s, %s: %s",
            message.guild,
            message.channel,
            message.author,
            message.content,
        )
