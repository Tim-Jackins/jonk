# Jonk

## Setup

Make a .env file with:

```
DISCORD_TOKEN=<your token>
MAX_QUEUE_SIZE=50
```

## Install

Install needed packages using:

```
pipenv install
```

For handling streams install `ffmpeg`:

```
sudo apt install ffmpeg
```

## Usage

```
make run
```

### Docker

The bot can run in docker but there have been issues so that deployment strategy isn't reliable right now.

### Formatting / Lint

```
make format
make lint
```
