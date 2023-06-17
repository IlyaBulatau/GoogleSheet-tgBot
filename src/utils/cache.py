from aiogram.fsm.storage.redis import Redis
from config import config

from datetime import timedelta
from math import ceil

redis = Redis(host=config.REDIS_HOST)


class VipUserCache:

    def __init__(self):
        self.cache = redis

    
    async def add_vip_in_hash(self, user_id, status, day):
        user_ttl_time = await self.cache.ttl('vip_'+str(user_id))
        if user_ttl_time == -2:
            await self.cache.set('vip_'+str(user_id), status, ex=timedelta(days=day))
        else:
            day = int(day) + ceil(int(user_ttl_time) // 86400)
            await self.cache.set('vip_'+str(user_id), status, ex=timedelta(days=day))

    async def get_vip_in_hash(self, user_id):
        status = await self.cache.get('vip_'+str(user_id))
        return status

cache = VipUserCache()

    