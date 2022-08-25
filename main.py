"""Main file for the bot"""

import logging
import os

import discord
from discord.ext import commands

from cogs import CommandHandler, ErrorHandler, LoggingHandler, MusicHandler

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


def when_mentioned(bot, msg):
    """
    A callable that implements a command prefix equivalent to being mentioned.
    """
    return f"<@{bot.user.id}> "


client = discord.Client()
bot = commands.Bot(command_prefix=when_mentioned)

# Load all cogs
bot.add_cog(CommandHandler(bot))
bot.add_cog(ErrorHandler(bot))
bot.add_cog(LoggingHandler(bot))
bot.add_cog(MusicHandler(bot))


@bot.event
async def on_message(message: discord.Message):
    """
    Override default message processor to avoid dms
    """
    if isinstance(message.channel, discord.DMChannel) and ("!" in message.content):
        await message.channel.send("Sorry no dms :wink:")
        return
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
