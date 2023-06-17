from aiogram.fsm.storage.redis import Redis
from config import config

from datetime import timedelta

redis = Redis(host=config.REDIS_HOST)


class VipUserCache:

    def __init__(self):
        self.cache = redis

    
    async def add_vip_in_hash(self, user_id, status, day):
        await self.cache.set('vip_'+str(user_id), status, ex=timedelta(days=day))

    async def get_vip_in_hash(self, user_id):
        status = await self.cache.get('vip_'+str(user_id))
        return status

cache = VipUserCache()

    