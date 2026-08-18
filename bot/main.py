import os
import re
import logging

import discord

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord-bot")

TOKEN = os.environ["DISCORD_TOKEN"]

URL_PATTERN = re.compile(
    r"https://akizukidenshi\.com/catalog/g/g(\d{6})/"
)


def convert_url(match: re.Match) -> str:
    product_id = match.group(1)
    return f"https://akizukidenshi.com/img/goods/L/{product_id}.jpg"


intents = discord.Intents.default()
intents.message_content = True  # Developer PortalでもMESSAGE CONTENT INTENTを有効化する

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info("Logged in as %s", client.user)


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    matches = list(URL_PATTERN.finditer(message.content))
    if not matches:
        return

    converted = [convert_url(m) for m in matches]
    await message.channel.send("\n".join(converted))


client.run(TOKEN)
