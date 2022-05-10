"""Contains utility functions for jonk"""

import logging
import re
import asyncio
import youtube_dl
import discord
import requests
import pafy

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


YTDL_FORMAT_OPTIONS = {
    "format": "bestaudio/best",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    "source_address": "0.0.0.0",
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1" " -reconnect_delay_max 5",
    "options": "-vn",
}

youtube_dl.utils.bug_reports_message = lambda: ""

ytdl = youtube_dl.YoutubeDL(YTDL_FORMAT_OPTIONS)


def is_youtube(url: str) -> bool:
    """
    Checks some heuristics to see if the given URL would resolve to a Youtube
    video.
    """
    youtube_start: str = "https://www.youtube.com/watch?v="
    return len(url) > len(youtube_start) and url[: len(youtube_start)] == youtube_start


async def filename_from_url(url, *, loop=None, stream=False):
    """Get youtube video filename to download"""
    loop = loop or asyncio.get_event_loop()
    data = await loop.run_in_executor(
        None, lambda: ytdl.extract_info(url, download=not stream)
    )
    if "entries" in data:
        # take first item from a playlist
        data = data["entries"][0]
    filename = data["title"] if stream else ytdl.prepare_filename(data)
    return filename


async def get_source(url: str, download: bool = False):
    """Returns discord bot music source from url"""
    if download:
        filename = await filename_from_url(url, loop=None)
        info = ytdl.extract_info(url, download=False)
        i_url = info["formats"][0]["url"]
        source = discord.FFmpegPCMAudio(executable="ffmpeg", source=filename)
    else:
        if is_youtube(url):
            video = pafy.new(url)
            best = video.getbestaudio()
            i_url = best.url
        else:
            logger.debug("Using non-youtube URL")
            i_url = url
        source = await discord.FFmpegOpusAudio.from_probe(i_url, **FFMPEG_OPTIONS)
    return source


async def get_yt_result_url(query: str):
    """Find video url using youtube's search function"""
    search_base = "https://www.youtube.com/results?search_query="
    video_base = "https://www.youtube.com/watch?v="

    scrape_url = f"{search_base}{query}"
    response = requests.get(scrape_url)

    result_video_ids = re.findall(r'{"url":"\/watch?\?v=(.*?)"', response.text)
    result_video_id = result_video_ids[0]
    result_video_url = f"{video_base}{result_video_id}"

    return result_video_url
