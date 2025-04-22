import redis.asyncio as redis
from src.config import Config

JTI_EXPIRES = 3600

token_redis = redis.Redis(
    host=Config.RADIS_HOST,
    port=Config.RADIS_PORT,
    db=0,
)

async def set_token(jti: str) -> None:
    await token_redis.set(name=jti, value="", ex=JTI_EXPIRES)

async def get_token(jti: str) -> bool:
    value = await token_redis.get(jti)
    return value is not None