import discord
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import asyncio


# Config
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


# Config
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


# General commands
from cogs import general_commands, Music

for command in general_commands:
    bot.add_command(command)

bot.add_cog(Music(bot))


if __name__ == "__main__" :
    bot.run(DISCORD_TOKEN)
