"""Main file for the bot"""

import asyncio
import logging
import os

import discord
from discord.ext import commands

from cogs import CommandHandler, ErrorHandler, LoggingHandler, MusicHandler, QrHandler

logger = logging.getLogger(__name__)
logging.basicConfig()
match os.getenv("LOG_LEVEL"):
    case "CRITICAL":
        logger.setLevel(logging.CRITICAL)
    case "FATAL":
        logger.setLevel(logging.FATAL)
    case "ERROR":
        logger.setLevel(logging.ERROR)
    case "WARNING":
        logger.setLevel(logging.WARNING)
    case "WARN":
        logger.setLevel(logging.WARN)
    case "INFO":
        logger.setLevel(logging.INFO)
    case "DEBUG":
        logger.setLevel(logging.DEBUG)
    case _:
        raise f"{os.getenv('LOG_LEVEL')} is invalid"

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

def when_mentioned(bot, msg):
    """
    A callable that implements a command prefix equivalent to being mentioned.
    """
    return f"<@{bot.user.id}> "

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(intents=intents, command_prefix=when_mentioned)

async def load_cogs():
    """Load all cogs asynchronously."""
    await bot.add_cog(CommandHandler(bot))
    await bot.add_cog(ErrorHandler(bot))
    await bot.add_cog(LoggingHandler(bot))
    # await bot.add_cog(MusicHandler(bot))
    await bot.add_cog(QrHandler(bot))

@bot.event
async def on_message(message: discord.Message):
    """
    Override default message processor to avoid dms
    """
    if isinstance(message.channel, discord.DMChannel) and ("!" in message.content):
        await message.channel.send("Sorry no dms :wink:")
        return
    await bot.process_commands(message)

async def main():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
