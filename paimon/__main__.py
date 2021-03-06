import asyncio
import discord
from discord import Message
from discord.utils import get
import logging.config
import yaml

from config import config_add, config
from vault import vault_init

config_add('./config.yaml')
config_add('./env_config.yaml')
vault_init(override=True)

#
# Logger Configuration
#
with open('logging.yaml', 'r') as lf:
    log_cfg = yaml.safe_load(lf.read())
logging.config.dictConfig(log_cfg)

log = logging.getLogger(__name__)

client = discord.Client()


async def organic_send(channel, *args, organic_time=None, **kwargs):
    async with channel.typing():
        if organic_time is None:
            organic_time = 1
        await asyncio.sleep(organic_time)
        await channel.send(*args, **kwargs)


@client.event
async def on_ready():
    log.info(f'Connected to Discord as {client.user}')


@client.event
async def on_message(message: Message):
    if get(message.mentions, id=client.user.id) is not None:
        await organic_send(message.channel, 'Hello')

client.run(config.bot_token(None))
