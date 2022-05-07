# Jonk

## Setup

Make a .env file with:

```
DISCORD_TOKEN=<your token>
MAX_QUEUE_SIZE=50
```

pipenv install -e git+https://github.com/explosion/spaCy#egg=spacy

pipenv install --dev -e "git+https://github.com/Tim-Jackins/pafy#egg=pafy"

pipenv run pip install "git+https://github.com/Tim-Jackins/pafy#egg_info=pafy"

py -m pip install "discord discord.py[voice] python-dotenv youtube-dl requests"



WARNING:discord.gateway:Shard ID None voice heartbeat blocked for more than 10 seconds
Loop thread traceback (most recent call last):
  File "main.py", line 34, in <module>
  File "/home/jack/.local/share/virtualenvs/jonk-eYmJZG_u/lib/python3.8/site-packages/discord/client.py", line 713, in run
    loop.run_forever()
  File "/usr/lib/python3.8/asyncio/base_events.py", line 570, in run_forever
    self._run_once()
  File "/usr/lib/python3.8/asyncio/base_events.py", line 1859, in _run_once
    handle._run()
  File "/usr/lib/python3.8/asyncio/events.py", line 81, in _run
    self._context.run(self._callback, *self._args)
  File "/home/jack/.local/share/virtualenvs/jonk-eYmJZG_u/lib/python3.8/site-packages/discord/ext/tasks/__init__.py", line 101, in _loop
    await self.coro(*args, **kwargs)
  File "/home/jack/Documents/discord/jonk/cogs/music.py", line 122, in next_song_checker
    next_song_url = q.get()
  File "/usr/lib/python3.8/queue.py", line 170, in get
    self.not_empty.wait()
  File "/usr/lib/python3.8/threading.py", line 302, in wait
    waiter.acquire()

WARNING:discord.gateway:Shard ID None voice heartbeat blocked for more than 20 seconds
Loop thread traceback (most recent call last):
  File "main.py", line 34, in <module>
  File "/home/jack/.local/share/virtualenvs/jonk-eYmJZG_u/lib/python3.8/site-packages/discord/client.py", line 713, in run
    loop.run_forever()
  File "/usr/lib/python3.8/asyncio/base_events.py", line 570, in run_forever
    self._run_once()
  File "/usr/lib/python3.8/asyncio/base_events.py", line 1859, in _run_once
    handle._run()
  File "/usr/lib/python3.8/asyncio/events.py", line 81, in _run
    self._context.run(self._callback, *self._args)
  File "/home/jack/.local/share/virtualenvs/jonk-eYmJZG_u/lib/python3.8/site-packages/discord/ext/tasks/__init__.py", line 101, in _loop
    await self.coro(*args, **kwargs)
  File "/home/jack/Documents/discord/jonk/cogs/music.py", line 122, in next_song_checker
    next_song_url = q.get()
  File "/usr/lib/python3.8/queue.py", line 170, in get
    self.not_empty.wait()
  File "/usr/lib/python3.8/threading.py", line 302, in wait
    waiter.acquire()

WARNING:discord.gateway:Shard ID None voice heartbeat blocked for more than 30 seconds
Loop thread traceback (most recent call last):
  File "main.py", line 34, in <module>
  File "/home/jack/.local/share/virtualenvs/jonk-eYmJZG_u/lib/python3.8/site-packages/discord/client.py", line 713, in run
    loop.run_forever()
  File "/usr/lib/python3.8/asyncio/base_events.py", line 570, in run_forever
    self._run_once()
  File "/usr/lib/python3.8/asyncio/base_events.py", line 1859, in _run_once
    handle._run()
  File "/usr/lib/python3.8/asyncio/events.py", line 81, in _run
    self._context.run(self._callback, *self._args)
  File "/home/jack/.local/share/virtualenvs/jonk-eYmJZG_u/lib/python3.8/site-packages/discord/ext/tasks/__init__.py", line 101, in _loop
    await self.coro(*args, **kwargs)
  File "/home/jack/Documents/discord/jonk/cogs/music.py", line 122, in next_song_checker
    next_song_url = q.get()
  File "/usr/lib/python3.8/queue.py", line 170, in get
    self.not_empty.wait()
  File "/usr/lib/python3.8/threading.py", line 302, in wait
    waiter.acquire()

^CWARNING:discord.gateway:Shard ID None voice heartbeat blocked for more than 40 seconds
Loop thread traceback (most recent call last):
  File "main.py", line 34, in <module>
  File "/home/jack/.local/share/virtualenvs/jonk-eYmJZG_u/lib/python3.8/site-packages/discord/client.py", line 713, in run
    loop.run_forever()
  File "/usr/lib/python3.8/asyncio/base_events.py", line 570, in run_forever
    self._run_once()
  File "/usr/lib/python3.8/asyncio/base_events.py", line 1859, in _run_once
    handle._run()
  File "/usr/lib/python3.8/asyncio/events.py", line 81, in _run
    self._context.run(self._callback, *self._args)
  File "/home/jack/.local/share/virtualenvs/jonk-eYmJZG_u/lib/python3.8/site-packages/discord/ext/tasks/__init__.py", line 101, in _loop
    await self.coro(*args, **kwargs)
  File "/home/jack/Documents/discord/jonk/cogs/music.py", line 122, in next_song_checker
    next_song_url = q.get()
  File "/usr/lib/python3.8/queue.py", line 170, in get
    self.not_empty.wait()
  File "/usr/lib/python3.8/threading.py", line 302, in wait
    waiter.acquire()
