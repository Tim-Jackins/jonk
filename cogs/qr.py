"""Conatains the cog for handling music commands"""
# pylint: disable=no-self-use

import logging
import asyncio
import os
import tempfile
import requests
import discord
from discord.ext import commands
from amzqr import amzqr
from urllib.parse import urlparse

from .utils import is_youtube, get_source, get_yt_result_url

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv('LOG_LEVEL'))

class QrHandler(commands.Cog):
    """Cog for handling qr commands"""

    def __init__(self, bot):
        self.bot = bot

    # 1 per user per 2s
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(name="qr")
    async def qr(
        self,
        ctx,
        data: str = commands.parameter(                           description="(string)       Data to be encoded"),
        version: int = commands.parameter(         default=1,     description="(int)          Version {1,2,3,...,40}"),
        error_correction: str = commands.parameter(default="H",   description="(char)         Error correction level {L,M,Q,H}"),
        image_url: str = commands.parameter(       default="",    description="(url|attached) Background image / gif. Specify 'attached' and then paste an image to use that."),
        colorized: bool = commands.parameter(      default=False, description="(boolean)      Colorize the qrcode?"),
        contrast: float = commands.parameter(      default=1.0,   description="(number)       Contrast of the qr code image"),
        brightness: float = commands.parameter(    default=1.0,   description="(number)       Brightness of the qr code image"),
    ):
        """Generates a qr code"""

        with tempfile.TemporaryDirectory() as temp_dir_name:
            background_picture = None
            if image_url != "":
                if image_url == "attached":
                    image_urls = []

                    # Get images from attachments
                    for attachment in ctx.message.attachments:
                        if attachment.content_type and attachment.content_type.startswith("image/"):
                            image_url = attachment.url

                    image_filename = os.path.basename(urlparse(image_url).path)
                    image_filepath = os.path.join(temp_dir_name, image_filename)
                    image_result = requests.get(image_url)
                logger.debug(f"Creating input image {image_filepath}")
                with open(image_filepath, "wb") as f:
                    f.write(image_result.content)
                background_picture = image_filepath

            version, level, qr_name = amzqr.run(
                data,
                version=version,
                level=error_correction,
                picture=background_picture,
                colorized=colorized,
                contrast=contrast,
                brightness=brightness,
                save_name=None,
                save_dir=temp_dir_name
            )

            logger.debug(temp_dir_name)
            logger.debug(os.listdir(temp_dir_name))

            qrimage_filename = "qrcode.png"
            if background_picture is not None:
                qrimage_filename = "".join(image_filename.split(".")[:-1]) + "_qrcode." + image_filename.split(".")[-1]

            qrimage_filepath = os.path.join(temp_dir_name, qrimage_filename)
            logger.debug(f"Creating input image {qrimage_filepath}")
            with open(qrimage_filepath, 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)

            await ctx.send(
                f"Generated with level {level} using the wonderful amzqr@{version}"
            )
