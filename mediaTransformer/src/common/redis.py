from src.common.env import settings
import redis.asyncio as redis

def get_redis():
    try:
        r = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            decode_responses=True,
            db=2
        )
        r.ping()
        print('Connected to redis!')
        return r
    except Exception as e:
        raise Exception('Failed to connect to redis:', e)

r=get_redis()
