import logging
from typing import *

import aioredis
from aioredis.client import Redis
from app.settings import Settings, get_settings

settings: Settings = get_settings()


async def get_redis_con() -> Redis:
    return aioredis.from_url(f"redis://{settings.REDIS_SERVER}", encoding="utf-8", decode_responses=True)
