from fastapi import APIRouter

from app.cache.factory import CacheFactory

router = APIRouter()


@router.get("/remember")
def api_remember():
    def return_version():
        print("returned no cached version")
        return "1.0.0"

    cache = CacheFactory.get_cache()
    cache.connect()

    version = cache.remember("brain_x_version", 3600, func=return_version)

    return {
        "version": version
    }


@router.get("/set")
def api_set():
    cache = CacheFactory.get_cache()
    cache.connect()

    key = "set_key"

    cache.set(key, "123")

    value = cache.get(key)

    return {
        "key": key,
        "value": value,
    }


@router.get("/a-set")
async def api_a_set():
    cache = CacheFactory.get_cache()

    key = "a_set_key"
    await cache.a_set(key, 123321)
    value = await cache.a_get(key)

    return {
        "key": key,
        "value": value,
    }
